import { Brain, GitCompareArrows, Quote, FileCheck } from "lucide-react";

const features = [
  {
    icon: Brain,
    title: "AI-Powered Eligibility Analysis",
    description: "Advanced language models parse scholarship criteria and match them against your profile instantly.",
  },
  {
    icon: GitCompareArrows,
    title: "Gap Analysis with Roadmap",
    description: "See exactly where you fall short and get actionable steps to close the gap before deadlines.",
  },
  {
    icon: Quote,
    title: "Source-Cited Explanations",
    description: "Every decision is backed by exact passages from the original document — no black boxes.",
  },
  {
    icon: FileCheck,
    title: "Works with Any Scholarship PDF",
    description: "Upload documents from any institution, foundation, or government program worldwide.",
  },
];

const FeaturesSection = () => {
  return (
    <section id="features" className="section-padding">
      <div className="container-wide">
        <div className="text-center max-w-2xl mx-auto mb-14">
          <p className="text-sm font-medium text-accent-foreground mb-3">Features</p>
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Everything you need to apply with confidence
          </h2>
          <p className="text-muted-foreground text-lg">
            Built for students who want clarity, not guesswork.
          </p>
        </div>
        <div className="grid sm:grid-cols-2 gap-5 max-w-4xl mx-auto">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="bg-card rounded-xl p-6 shadow-card hover:shadow-card-hover transition-shadow duration-300 border border-border/50"
            >
              <div className="w-10 h-10 rounded-lg bg-primary-soft flex items-center justify-center mb-4">
                <feature.icon className="w-5 h-5 text-accent-foreground" />
              </div>
              <h3 className="font-semibold text-foreground mb-2">{feature.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
