import { Button } from "@/components/ui/button";
import { ArrowRight, Upload } from "lucide-react";
import heroIllustration from "@/assets/hero-illustration.png";

const HeroSection = () => {
  return (
    <section className="section-padding pt-32 md:pt-40">
      <div className="container-wide">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <div className="max-w-xl">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-primary-soft text-accent-foreground text-sm font-medium mb-6">
              <span className="w-2 h-2 rounded-full bg-primary" />
              AI-Powered Scholarship Intelligence
            </div>
            <h1 className="text-4xl md:text-5xl lg:text-[3.25rem] font-bold leading-[1.15] mb-5 text-foreground">
              Turn Complex Scholarship Rules Into Clear Answers
            </h1>
            <p className="text-lg text-muted-foreground leading-relaxed mb-8">
              Scholara uses AI to analyze official scholarship PDFs and provide instant eligibility decisions — with clear explanations and actionable next steps.
            </p>
            <div className="flex flex-wrap gap-3">
              <Button 
              onClick={() => window.location.href = "http://localhost:5000/analyze"}
            
              size="lg" className="gap-2">
                Try It Now <ArrowRight className="w-4 h-4" />
              </Button>
              <Button 
              onClick={() => window.location.href = "http://localhost:5000/pdf"}
            
              size="lg" variant="outline" className="gap-2">
                <Upload className="w-4 h-4" /> Upload Scholarship
              </Button>
            </div>
          </div>
          <div className="relative">
            <div className="rounded-2xl overflow-hidden shadow-card">
              <img
                src={heroIllustration}
                alt="AI document analysis illustration"
                className="w-full h-auto"
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
