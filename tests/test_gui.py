import unittest
import tkinter as tk
from gui.main_window import MainApp

class TestGUI(unittest.TestCase):
    def setUp(self):
        try: self.app=MainApp()
        except tk.TclError as e: self.skipTest(str(e))
        self.app.update()
    def tearDown(self):
        if hasattr(self,'app'): self.app.destroy()
    def widgets(self,root,kind):
        return [w for child in root.winfo_children() for w in ([child] if isinstance(child,kind) else [])+self.widgets(child,kind)]
    def click(self,root,name):
        next(b for b in self.widgets(root,tk.Button) if b.cget('text')==name).invoke()
        self.app.update()
    def test_navigation_and_resize(self):
        for size in ('900x600','1180x800','1500x900'):
            self.app.geometry(size)
            for name in self.app.pages:
                self.app.show(name); self.app.update()
                self.assertTrue(self.app.views[name].winfo_ismapped())
    def test_aes_ui_round_trip(self):
        self.app.show('AES Encryption'); root=self.app.views['AES Encryption']
        inp,out=self.widgets(root,tk.Text)
        self.click(root,'Generate key'); inp.insert('1.0','Hello world'); self.click(root,'Encrypt')
        self.assertTrue(self.app.read(out)); self.click(root,'Use output as input'); self.click(root,'Decrypt')
        self.assertEqual(self.app.read(out),'Hello world')
        self.app.show('Dashboard'); self.app.show('AES Encryption'); self.assertEqual(self.app.read(out),'Hello world')
    def test_secret_ui(self):
        self.app.show('Secret Generator'); root=self.app.views['Secret Generator']; self.click(root,'Random hex')
        self.assertEqual(len(self.app.read(self.widgets(root,tk.Text)[0])),64)
