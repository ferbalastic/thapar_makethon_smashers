import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

const CTASection = () => {
  return (
    <section className="section-padding">
      <div className="container-narrow">
        <div className="bg-primary rounded-2xl p-10 md:p-16 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-primary-foreground mb-4">
            Stop Guessing. Start Applying Strategically.
          </h2>
          <p className="text-primary-foreground/80 text-lg mb-8 max-w-lg mx-auto">
            Upload a scholarship PDF and get your eligibility report in under a minute.
          </p>
          <Button
            onClick={() => window.location.href = "http://localhost:5000/analyze"}
            size="lg"
            variant="secondary"
            className="gap-2 font-semibold"
          >
            Check My Eligibility <ArrowRight className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </section>
  );
};

export default CTASection;
