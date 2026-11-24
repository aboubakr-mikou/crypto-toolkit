"""Dark, offline desktop workbench."""
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import base64, secrets, hmac, hashlib
from pathlib import Path
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import serialization
from core import toolkit as tools
from core.asymmetric import AsymmetricCipher
from core.signature import DigitalSignature

BG='#090E17'; PANEL='#121E2D'; FIELD='#1A303B'; TEXT='#F1F5F9'; MUTED='#A4B2C4'; ACCENT='#2DD4BF'; BORDER='#253346'

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__(); self.title('CryptoToolkit | Security Workbench'); self.geometry('1180x800'); self.minsize(900,600); self.configure(bg=BG)
        self.rsa=AsymmetricCipher(); self.sig=DigitalSignature(); self.cert_key=None; self.cert_pem=None
        self.icons={}; self.make_icons()
        self.iconphoto(True,self.icons['shield'])
        top=tk.Frame(self,bg=PANEL,height=62); top.pack(fill='x'); top.pack_propagate(False)
        tk.Label(top,image=self.icons['shield'],bg=PANEL).pack(side='left',padx=(20,8))
        self.label(top,'CryptoToolkit',19,TEXT,True).pack(side='left'); self.label(top,'  /  v2.0',10,MUTED).pack(side='left')
        self.label(top,'●  OFFLINE MODE',10,ACCENT,True).pack(side='right',padx=24)
        shell=tk.Frame(self,bg=BG); shell.pack(fill='both',expand=True)
        self.nav=tk.Frame(shell,bg=PANEL,width=230); self.nav.pack(side='left',fill='y'); self.nav.pack_propagate(False)
        self.label(self.nav,'WORKSPACE',10,MUTED,True).pack(anchor='w',padx=20,pady=(22,12))
        self.pages={'Dashboard':self.home,'AES Encryption':self.aes,'RSA Toolkit':self.rsa_page,'Hash Analyzer':self.hash_page,'Digital Signatures':self.signature,'Certificates':self.certificate,'Encoder':self.utilities,'Secret Generator':self.secret_page,'About':self.about}
        self.page_icons=dict(zip(self.pages,['grid','lock','key','hash','sign','cert','code','shield','info']))
        self.nav_buttons={}
        for name in self.pages:
            b=tk.Button(self.nav,text='  '+name,image=self.icons[self.page_icons[name]],compound='left',anchor='w',bg=PANEL,fg=TEXT,activebackground=FIELD,activeforeground=ACCENT,relief='flat',bd=0,highlightthickness=0,font=('Segoe UI',11),padx=14,pady=9,cursor='hand2',command=lambda n=name:self.show(n)); b.pack(fill='x',padx=10,pady=2); self.nav_buttons[name]=b
        self.label(self.nav,'LOCAL WORKSPACE',9,MUTED).pack(side='bottom',anchor='w',padx=20,pady=16)
        right=tk.Frame(shell,bg=BG); right.pack(side='left',fill='both',expand=True)
        bottom=tk.Frame(right,bg=PANEL); bottom.pack(side='bottom',fill='x',padx=18,pady=(0,12))
        self.status=tk.StringVar(value='READY / Local processing only'); self.status_label=tk.Label(bottom,textvariable=self.status,bg=PANEL,fg=ACCENT,anchor='w',padx=12,pady=10,justify='left',wraplength=550); self.status_label.pack(fill='x')
        style=ttk.Style(self); style.theme_use('clam'); style.configure('Vertical.TScrollbar',background=FIELD,troughcolor=BG,bordercolor=BG,arrowcolor=MUTED,lightcolor=FIELD,darkcolor=FIELD); style.configure('TCombobox',fieldbackground=FIELD,background=PANEL,foreground=TEXT,arrowcolor=TEXT); style.map('TCombobox',fieldbackground=[('readonly',FIELD)],foreground=[('readonly',TEXT)]); self.canvas=tk.Canvas(right,bg=BG,highlightthickness=0); scrollbar=ttk.Scrollbar(right,orient='vertical',command=self.canvas.yview); scrollbar.pack(side='right',fill='y'); self.canvas.pack(side='left',fill='both',expand=True,padx=(18,0),pady=12); self.canvas.configure(yscrollcommand=scrollbar.set)
        self.host=tk.Frame(self.canvas,bg=BG); self.window=self.canvas.create_window((0,0),window=self.host,anchor='nw'); self.host.bind('<Configure>',lambda e:self.canvas.configure(scrollregion=self.canvas.bbox('all'))); self.canvas.bind('<Configure>',lambda e:self.canvas.itemconfigure(self.window,width=e.width))
        self.bind_all('<MouseWheel>',self.wheel); self.bind_all('<Button-4>',self.wheel); self.bind_all('<Button-5>',self.wheel)
        self.views={}; self.show('Dashboard')
    def wheel(self,event):
        if isinstance(event.widget,tk.Text): return
        self.canvas.yview_scroll(-1 if getattr(event,'num',0)==4 or getattr(event,'delta',0)>0 else 1,'units')
    def make_icons(self):
        # Small vector line icons; no external assets or emoji fonts required.
        paths={'shield':[(12,2,21,6,20,15,12,22,4,15,3,6,12,2),(7,12,11,16,17,9)],'grid':[(3,3,10,3,10,10,3,10,3,3),(14,3,21,3,21,10,14,10,14,3),(3,14,10,14,10,21,3,21,3,14),(14,14,21,14,21,21,14,21,14,14)],'lock':[(5,10,19,10,19,22,5,22,5,10),(8,10,8,5,12,2,16,5,16,10),(12,14,12,18)],'key':[(3,7,7,3,12,3,16,7,12,11,7,11,3,7),(13,10,22,19,19,22,16,19,18,17)],'hash':[(9,3,5,21),(18,3,14,21),(3,9,22,9),(2,15,21,15)],'sign':[(3,21,8,20,21,7,17,3,4,16,3,21),(14,6,18,10)],'cert':[(4,2,20,2,20,18,4,18,4,2),(7,7,17,7),(7,11,17,11),(9,18,9,23,12,21,15,23,15,18)],'code':[(8,5,2,12,8,19),(16,5,22,12,16,19),(14,3,10,21)],'info':[(12,3,19,6,22,12,19,19,12,22,5,19,2,12,5,6,12,3),(12,10,12,17),(12,6,12,7)]}
        for name,lines in paths.items():
            im=tk.PhotoImage(width=24,height=24)
            for line in lines:
                for x,y,u,v in zip(line[::2],line[1::2],line[2::2],line[3::2]):
                    n=max(abs(u-x),abs(v-y),1)
                    for j in range(n+1):
                        a=round(x+(u-x)*j/n); b=round(y+(v-y)*j/n); im.put(ACCENT,to=(a,b,min(a+2,24),min(b+2,24)))
            self.icons[name]=im
    def label(self,parent,text,size=11,color=TEXT,bold=False):
        return tk.Label(parent,text=text,bg=parent.cget('bg'),fg=color,font=('Segoe UI',size,'bold' if bold else 'normal'),anchor='w',justify='left')
    def show(self,name):
        for w in self.host.winfo_children(): w.pack_forget()
        for n,b in self.nav_buttons.items(): b.configure(bg=FIELD if n==name else PANEL,fg=ACCENT if n==name else TEXT)
        if name not in self.views:
            self.body=tk.Frame(self.host,bg=BG,padx=10,pady=8); self.views[name]=self.body; self.pages[name]()
        self.views[name].pack(fill='both',expand=True); self.canvas.yview_moveto(0); self.status.set('READY / '+name); self.status_label.configure(fg=ACCENT)
    def header(self,title,subtitle):
        self.label(self.body,title,25,TEXT,True).pack(anchor='w'); sub=self.label(self.body,subtitle,11,MUTED); sub.configure(wraplength=560); sub.pack(anchor='w',pady=(5,18)); self.panel=tk.Frame(self.body,bg=PANEL,padx=18,pady=16,highlightbackground=BORDER,highlightthickness=1); self.panel.pack(fill='both',expand=True)
    def entry(self,title,secret=False):
        self.label(self.panel,title,10,MUTED,True).pack(anchor='w',pady=(5,3)); e=tk.Entry(self.panel,bg=FIELD,fg=TEXT,insertbackground=TEXT,relief='flat',bd=0,highlightthickness=0,font=('Consolas',11),show='*' if secret else ''); e.pack(fill='x',ipady=7); return e
    def area(self,title,height=4):
        self.label(self.panel,title,10,MUTED,True).pack(anchor='w',pady=(8,3)); t=tk.Text(self.panel,height=height,bg=FIELD,fg=TEXT,insertbackground=TEXT,relief='flat',bd=0,highlightthickness=0,font=('Consolas',11),wrap='word',padx=8,pady=6); t.pack(fill='both',expand=True); return t
    def buttons(self,*actions):
        row=tk.Frame(self.panel,bg=PANEL); row.pack(fill='x',pady=7)
        for i,(name,fn) in enumerate(actions):
            tk.Button(row,text=name,command=lambda f=fn:self.run(f),bg=ACCENT if i==0 else FIELD,fg=BG if i==0 else TEXT,activebackground=BORDER,activeforeground=TEXT,relief='flat',bd=0,highlightthickness=0,padx=12,pady=7,font=('Segoe UI',10,'bold'),cursor='hand2').grid(row=i//3,column=i%3,sticky='w',padx=(0,6),pady=3)
    def run(self,fn):
        try: fn(); self.status.set('OK  /  Operation completed'); self.status_label.configure(fg=ACCENT)
        except InvalidTag: self.status.set('ERROR  /  Authentication failed: wrong key or modified ciphertext'); self.status_label.configure(fg='#FCA5A5')
        except Exception as e: self.status.set('ERROR  /  '+(str(e) or type(e).__name__)); self.status_label.configure(fg='#FCA5A5')
    @staticmethod
    def read(t): return t.get('1.0','end-1c')
    @staticmethod
    def put(t,s): t.delete('1.0','end'); t.insert('1.0',s)
    def export_text(self,t):
        if not messagebox.askyesno('Export output','Output may contain sensitive data. Save to a local text file?'): return
        path=filedialog.asksaveasfilename(defaultextension='.txt',filetypes=[('Text files','*.txt'),('All files','*')])
        if path: Path(path).write_text(self.read(t),encoding='utf-8')
    def input_tools(self,t,out=None):
        def load():
            path=filedialog.askopenfilename()
            if path:
                p=Path(path)
                if p.stat().st_size>2*1024*1024: raise ValueError('Text imports are limited to 2 MiB.')
                self.put(t,p.read_text(encoding='utf-8'))
        actions=[('Import text',load),('Clear input',lambda:self.put(t,''))]
        if out is not None: actions.append(('Use output as input',lambda:self.put(t,self.read(out))))
        self.buttons(*actions)
    def output(self,t):
        self.buttons(('Copy output',lambda:(self.clipboard_clear(),self.clipboard_append(self.read(t)))),('Clear output',lambda:self.put(t,'')),('Export output',lambda:self.export_text(t)))
    def home(self):
        self.header('Security Dashboard','Your offline cryptographic workspace.')
        self.panel.configure(bg=BG,highlightthickness=0,padx=0,pady=0)
        stats=tk.Frame(self.panel,bg=BG); stats.pack(fill='x',pady=(0,18))
        for i,(title,value) in enumerate([('Security modules','7'),('Processing','Local'),('Connection','Offline')]):
            stats.columnconfigure(i,weight=1,uniform='stats'); card=tk.Frame(stats,bg=PANEL,padx=12,pady=12,highlightbackground=BORDER,highlightthickness=1); card.grid(row=0,column=i,sticky='nsew',padx=4); self.label(card,value,20,ACCENT,True).pack(anchor='w'); self.label(card,title,10,MUTED).pack(anchor='w')
        self.label(self.panel,'Security Tools',16,TEXT,True).pack(anchor='w',pady=(0,10))
        grid=tk.Frame(self.panel,bg=BG); grid.pack(fill='x'); grid.columnconfigure(0,weight=1,uniform='cards'); grid.columnconfigure(1,weight=1,uniform='cards')
        for i,(name,desc) in enumerate([('AES Encryption','Authenticated AES-256-GCM'),('RSA Toolkit','Asymmetric encryption / OAEP'),('Hash Analyzer','Text and file fingerprints'),('Digital Signatures','Sign and verify messages'),('Certificates','X.509 certificate inspection'),('Encoder','Base64, hex and HMAC utilities'),('Secret Generator','Cryptographically random secrets')]):
            card=tk.Frame(grid,bg=PANEL,padx=14,pady=8,highlightbackground=BORDER,highlightthickness=1); card.grid(row=i//2,column=i%2,sticky='nsew',padx=4,pady=4)
            heading=tk.Frame(card,bg=PANEL); heading.pack(fill='x'); tk.Label(heading,image=self.icons[self.page_icons[name]],bg=PANEL).pack(side='left',padx=(0,8)); self.label(heading,name,13,TEXT,True).pack(side='left'); lab=self.label(card,desc,10,MUTED); lab.configure(wraplength=220); lab.pack(anchor='w'); tk.Button(card,text='Open tool  →',command=lambda n=name:self.show(n),bg=PANEL,fg=ACCENT,activebackground=FIELD,activeforeground=ACCENT,relief='flat',bd=0,highlightthickness=0,cursor='hand2',font=('Segoe UI',10,'bold')).pack(anchor='w',pady=(3,0))
        self.label(self.panel,'Educational toolkit • No network requests • No telemetry',10,MUTED).pack(anchor='w',pady=15)
    def secret_page(self):
        self.header('Secret Generator','Generate cryptographically random values using Python secrets.')
        length=self.entry('LENGTH / bytes (16–128)'); length.insert(0,'32'); out=self.area('GENERATED SECRET',5)
        def gen(kind):
            n=int(length.get())
            if not 16<=n<=128: raise ValueError('Choose 16–128 bytes.')
            self.put(out,secrets.token_hex(n) if kind=='hex' else secrets.token_urlsafe(n))
        self.buttons(('Random hex',lambda:gen('hex')),('URL-safe token',lambda:gen('url'))); self.output(out)
    def about(self):
        self.header('About CryptoToolkit','Version 2.0 / Local Security Workbench')
        for title,desc in [('Developer','Aboubakr Mikou — Computer Science Engineering Student, ENSA Fès'),('Purpose','Educational cryptography and authorized security assessments.'),('Privacy','All operations run locally. No telemetry or network requests.'),('Limitations','Not independently audited. Not intended for production key management.')]:
            self.label(self.panel,title,14,ACCENT,True).pack(anchor='w',pady=(12,4)); lab=self.label(self.panel,desc,11); lab.configure(wraplength=500); lab.pack(anchor='w')
    def aes(self):
        self.header('AES-256-GCM','Authenticated encryption • random nonce • Base64 transport format')
        k=self.entry('KEY / 64 hexadecimal characters',True)
        def gen(): k.delete(0,'end'); k.insert(0,secrets.token_hex(32))
        self.buttons(('Generate key',gen),('Show / hide key',lambda:k.configure(show='' if k.cget('show') else '*')))
        inp=self.area('INPUT / plaintext or ciphertext'); out=self.area('OUTPUT')
        self.buttons(('Encrypt',lambda:self.put(out,tools.encrypt_text(k.get(),self.read(inp)))),('Decrypt',lambda:self.put(out,tools.decrypt_text(k.get(),self.read(inp)))))
        self.input_tools(inp,out); self.output(out)
    def rsa_page(self):
        self.header('RSA / OAEP','RSA-2048 • SHA-256 • small UTF-8 messages (max 190 bytes)')
        inp=self.area('INPUT / plaintext or hexadecimal ciphertext'); out=self.area('OUTPUT')
        self.buttons(('Generate session keys',self.rsa.generer_cles),('Encrypt',lambda:self.put(out,self.rsa.chiffrer(self.read(inp)) if self.rsa.cle_publique else (_ for _ in ()).throw(ValueError('Generate session keys first.')))),('Decrypt',lambda:self.put(out,self.rsa.dechiffrer(self.read(inp)) if self.rsa.cle_privee else (_ for _ in ()).throw(ValueError('Generate session keys first.')))))
        self.label(self.panel,'Keys remain in memory. Generating new keys replaces the previous pair.',10,MUTED).pack(anchor='w'); self.input_tools(inp,out); self.output(out)
    def hash_page(self):
        self.header('Hash & integrity','Compute fingerprints and compare with a trusted reference digest.')
        alg=tk.StringVar(value='sha256'); ttk.Combobox(self.panel,textvariable=alg,values=['sha256','sha512','sha1','md5'],state='readonly').pack(anchor='w')
        self.label(self.panel,'MD5 and SHA-1: legacy comparison only, not secure integrity.',10,MUTED).pack(anchor='w')
        inp=self.area('TEXT INPUT',3); expected=self.entry('EXPECTED DIGEST / optional'); out=self.area('RESULT',3)
        def verify():
            actual=self.read(out).strip(); ref=expected.get().strip().lower()
            if not actual or not ref: raise ValueError('Compute a digest and enter a reference first.')
            messagebox.showinfo('Integrity','MATCH' if hmac.compare_digest(actual,ref) else 'MISMATCH')
        def filehash():
            path=filedialog.askopenfilename();
            if path: self.put(out,tools.file_digest(path,alg.get()))
        self.buttons(('Hash text',lambda:self.put(out,tools.digest(self.read(inp).encode(),alg.get()))),('Hash file',filehash),('Compare',verify)); self.input_tools(inp); self.output(out)
    def signature(self):
        self.header('Digital signatures','RSA-PSS / SHA-256 • sign and verify with a session key pair')
        inp=self.area('MESSAGE',3); out=self.area('SIGNATURE / hexadecimal',5)
        def verify(): messagebox.showinfo('Signature','VALID' if self.sig.verify_signature(self.read(inp),bytes.fromhex(self.read(out))) else 'INVALID')
        self.buttons(('Generate session keys',self.sig.generate_key_pair),('Sign',lambda:self.put(out,self.sig.sign_message(self.read(inp)).hex())),('Verify',verify)); self.input_tools(inp); self.output(out)
    def certificate(self):
        self.header('X.509 certificates','Inspect local PEM / DER files or generate a self-signed lab certificate.')
        domain=self.entry('DNS NAME / e.g. lab.example'); out=self.area('CERTIFICATE DETAILS',9)
        def load():
            path=filedialog.askopenfilename();
            if path: self.put(out,tools.inspect_certificate(Path(path).read_bytes()))
        def gen():
            self.cert_key,self.cert_pem=tools.generate_certificate(domain.get().strip() or 'lab.example'); self.put(out,tools.inspect_certificate(self.cert_pem))
        def save():
            if not self.cert_pem: raise ValueError('Generate a certificate first.')
            path=filedialog.asksaveasfilename(defaultextension='.pem');
            if path: Path(path).write_bytes(self.cert_pem)
        def key():
            if not self.cert_key: raise ValueError('Generate a certificate first.')
            password=simpledialog.askstring('Encrypted private key','Enter a password (at least 12 characters)',show='*',parent=self)
            if not password or len(password)<12: raise ValueError('Password must contain at least 12 characters.')
            path=filedialog.asksaveasfilename(defaultextension='.pem');
            if path: Path(path).write_bytes(self.cert_key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.BestAvailableEncryption(password.encode())))
        self.buttons(('Inspect file',load),('Generate lab cert',gen)); self.buttons(('Save certificate',save),('Export encrypted key',key)); self.output(out)
    def utilities(self):
        self.header('Encoder & HMAC','Encoding is not encryption. HMAC authenticates data using a shared secret.')
        inp=self.area('INPUT',3); out=self.area('OUTPUT',3); key=self.entry('HMAC KEY / optional text secret',True)
        self.buttons(('Base64 encode',lambda:self.put(out,base64.b64encode(self.read(inp).encode()).decode())),('Base64 decode',lambda:self.put(out,base64.b64decode(self.read(inp),validate=True).decode())),('Hex encode',lambda:self.put(out,self.read(inp).encode().hex())),('Hex decode',lambda:self.put(out,bytes.fromhex(self.read(inp)).decode())))
        self.buttons(('HMAC-SHA256',lambda:self.put(out,hmac.new(key.get().encode(),self.read(inp).encode(),hashlib.sha256).hexdigest()) if key.get() else (_ for _ in ()).throw(ValueError('Enter an HMAC key.')))); self.input_tools(inp,out); self.output(out)
