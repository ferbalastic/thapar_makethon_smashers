import { FileText, HelpCircle, XCircle, Clock } from "lucide-react";

const problems = [
  {
    icon: FileText,
    title: "Buried in PDFs",
    description: "Eligibility rules are hidden across long, complex documents that are hard to parse.",
  },
  {
    icon: HelpCircle,
    title: "Uncertain Qualification",
    description: "Students can't tell if they qualify without reading every line of fine print.",
  },
  {
    icon: XCircle,
    title: "Unexplained Rejections",
    description: "Applications get rejected without clear feedback on what went wrong.",
  },
  {
    icon: Clock,
    title: "Wasted Time",
    description: "Hours spent applying to scholarships that were never a good fit to begin with.",
  },
];

const ProblemSection = () => {
  return (
    <section id="problem" className="section-padding">
      <div className="container-wide">
        <div className="text-center max-w-2xl mx-auto mb-14">
          <p className="text-sm font-medium text-accent-foreground mb-3">The Problem</p>
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Applying for scholarships shouldn't feel like guesswork
          </h2>
          <p className="text-muted-foreground text-lg">
            Most students waste time on scholarships they'll never receive — simply because the rules are too complex to understand.
          </p>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {problems.map((problem) => (
            <div
              key={problem.title}
              className="bg-card rounded-xl p-6 shadow-card hover:shadow-card-hover transition-shadow duration-300"
            >
              <div className="w-10 h-10 rounded-lg bg-primary-soft flex items-center justify-center mb-4">
                <problem.icon className="w-5 h-5 text-accent-foreground" />
              </div>
              <h3 className="font-semibold text-foreground mb-2">{problem.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{problem.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ProblemSection;
