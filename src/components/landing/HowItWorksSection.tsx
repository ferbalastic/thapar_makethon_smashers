import { FileSearch, Database, MessageSquareText } from "lucide-react";

const steps = [
  {
    icon: FileSearch,
    title: "Reads & Understands Documents",
    description: "Scholara's AI processes the full scholarship PDF, extracting every eligibility rule, deadline, and requirement.",
  },
  {
    icon: Database,
    title: "Retrieves Exact Rule Passages",
    description: "Using retrieval-augmented generation, it identifies the precise clauses relevant to your profile.",
  },
  {
    icon: MessageSquareText,
    title: "Generates Explainable Results",
    description: "You get a clear verdict — eligible or not — with cited evidence and specific recommendations.",
  },
];

const HowItWorksSection = () => {
  return (
    <section id="how-it-works" className="section-padding bg-card">
      <div className="container-wide">
        <div className="text-center max-w-2xl mx-auto mb-14">
          <p className="text-sm font-medium text-accent-foreground mb-3">How It Works</p>
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Intelligent analysis, not just keyword matching
          </h2>
          <p className="text-muted-foreground text-lg">
            Scholara goes beyond surface-level scanning to deeply understand what each scholarship requires.
          </p>
        </div>
        <div className="max-w-3xl mx-auto space-y-6">
          {steps.map((step, index) => (
            <div key={step.title} className="flex gap-5 items-start bg-background rounded-xl p-6 shadow-card">
              <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-primary flex items-center justify-center text-primary-foreground font-semibold text-sm">
                {index + 1}
              </div>
              <div>
                <h3 className="font-semibold text-foreground mb-1">{step.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorksSection;
