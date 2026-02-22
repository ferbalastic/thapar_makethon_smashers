import { Upload, UserCheck, CheckCircle } from "lucide-react";

const steps = [
  {
    icon: Upload,
    step: "01",
    title: "Upload Scholarship PDF",
    description: "Drop any official scholarship document — Scholara handles the rest.",
  },
  {
    icon: UserCheck,
    step: "02",
    title: "Enter Student Details",
    description: "Provide basic academic and personal info for accurate matching.",
  },
  {
    icon: CheckCircle,
    step: "03",
    title: "Get Instant Decision",
    description: "Receive a clear eligibility verdict with gap analysis and cited sources.",
  },
];

const SolutionSection = () => {
  return (
    <section id="solution" className="section-padding bg-card">
      <div className="container-wide">
        <div className="text-center max-w-2xl mx-auto mb-14">
          <p className="text-sm font-medium text-accent-foreground mb-3">The Solution</p>
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            From PDF to decision in under a minute
          </h2>
          <p className="text-muted-foreground text-lg">
            Scholara reads, understands, and evaluates scholarship documents so you don't have to.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mb-16">
          {steps.map((s) => (
            <div key={s.step} className="relative bg-background rounded-xl p-6 shadow-card">
              <span className="text-5xl font-bold text-primary/10 absolute top-4 right-5">{s.step}</span>
              <div className="w-10 h-10 rounded-lg bg-primary-soft flex items-center justify-center mb-4">
                <s.icon className="w-5 h-5 text-accent-foreground" />
              </div>
              <h3 className="font-semibold text-foreground mb-2">{s.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{s.description}</p>
            </div>
          ))}
        </div>

        {/* Mock UI Preview */}
        <div className="bg-background rounded-2xl shadow-card overflow-hidden border border-border max-w-3xl mx-auto">
          <div className="flex items-center gap-2 px-4 py-3 border-b border-border bg-muted/50">
            <div className="w-3 h-3 rounded-full bg-destructive/40" />
            <div className="w-3 h-3 rounded-full bg-yellow-400/40" />
            <div className="w-3 h-3 rounded-full bg-green-400/40" />
            <span className="ml-2 text-xs text-muted-foreground">scholara.ai/dashboard</span>
          </div>
          <div className="p-6 md:p-8">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h4 className="font-semibold text-foreground">Eligibility Report</h4>
                <p className="text-sm text-muted-foreground">National Merit Scholarship 2026</p>
              </div>
              <span className="px-3 py-1 rounded-full bg-green-100 text-green-700 text-sm font-medium">
                Eligible ✓
              </span>
            </div>
            <div className="space-y-3">
              {[
                { label: "GPA Requirement (≥ 3.5)", status: true, value: "3.8" },
                { label: "Enrollment Status (Full-time)", status: true, value: "Full-time" },
                { label: "Community Service (≥ 40 hrs)", status: false, value: "28 hrs" },
              ].map((rule) => (
                <div key={rule.label} className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                  <div className="flex items-center gap-3">
                    <div className={`w-2 h-2 rounded-full ${rule.status ? 'bg-green-500' : 'bg-amber-500'}`} />
                    <span className="text-sm text-foreground">{rule.label}</span>
                  </div>
                  <span className="text-sm text-muted-foreground">{rule.value}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default SolutionSection;
