const Footer = () => {
  return (
    <footer className="border-t border-border py-12 px-6">
      <div className="container-wide flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-primary flex items-center justify-center">
            <span className="text-primary-foreground font-bold text-xs">S</span>
          </div>
          <span className="font-semibold text-foreground">Scholara</span>
          <span className="text-muted-foreground text-sm ml-2">— Scholarship intelligence, simplified.</span>
        </div>
        <div className="flex items-center gap-6 text-sm text-muted-foreground">
          <a href="#" className="hover:text-foreground transition-colors">About</a>
          <a href="#" className="hover:text-foreground transition-colors">Contact</a>
          <a href="#" className="hover:text-foreground transition-colors">Privacy</a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
