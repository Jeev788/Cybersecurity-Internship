const FACTORS = [
  { key: "authentication", label: "Authentication", values: { MFA: 0, "SSO + MFA": 0, Password: 18, "Password + OTP": 8 } },
  { key: "authorization", label: "Authorization", values: { RBAC: 0, "Least Privilege": 0, "Role Based": 2, "Open Access": 18 } },
  { key: "encryption", label: "Encryption", values: { Enabled: 0, "At Rest + Transit": 0, "Transit Only": 8, Disabled: 20 } },
  { key: "logging", label: "Logging", values: { Enabled: 0, Centralized: 0, Basic: 7, Disabled: 15 } },
  { key: "monitoring", label: "Monitoring", values: { Enabled: 0, SIEM: 0, Basic: 6, Disabled: 14 } },
  { key: "exposure", label: "Internet Exposure", values: { Internal: 0, Private: 0, Restricted: 4, Internet: 16 } },
  { key: "sensitivity", label: "Data Sensitivity", values: { Public: 0, Internal: 5, Confidential: 12, Restricted: 18 } },
  { key: "backup", label: "Backup", values: { Verified: 0, Enabled: 2, Unverified: 7, Disabled: 13 } },
  { key: "patchAge", label: "Patch Age", values: { "0-7 days": 0, "8-30 days": 5, "31-90 days": 11, "90+ days": 18 } }
];

export const validCategories = ["Identity", "Network", "Application", "Data", "Endpoint", "Cloud"];
const severity = score => score >= 75 ? "CRITICAL" : score >= 55 ? "HIGH" : score >= 30 ? "MEDIUM" : "LOW";
const scoreFor = (factor, value) => factor.values[String(value)] ?? Math.max(...Object.values(factor.values));

export function calculateRisk(current = {}, proposed = {}) {
  let currentScore = 0;
  let projectedScore = 0;
  const factors = [];
  for (const factor of FACTORS) {
    const currentPoints = scoreFor(factor, current[factor.key]);
    const proposedPoints = scoreFor(factor, proposed[factor.key]);
    currentScore += currentPoints;
    projectedScore += proposedPoints;
    if (current[factor.key] !== proposed[factor.key]) {
      factors.push({
        name: factor.label,
        current: current[factor.key] ?? "Not specified",
        proposed: proposed[factor.key] ?? "Not specified",
        currentPoints, proposedPoints,
        impact: proposedPoints - currentPoints,
        reason: proposedPoints > currentPoints ? `${factor.label} becomes less protective.` : `${factor.label} becomes more protective.`
      });
    }
  }
  currentScore = Math.min(100, currentScore);
  projectedScore = Math.min(100, projectedScore);
  const recommendations = [];
  if (projectedScore >= 75) recommendations.push("Do not approve without compensating controls and security-owner approval.");
  if (proposed.authentication === "Password") recommendations.push("Keep MFA or phishing-resistant authentication for privileged or exposed users.");
  if (proposed.logging === "Disabled") recommendations.push("Retain centralized logging for investigations and evidence.");
  if (proposed.monitoring === "Disabled") recommendations.push("Keep monitoring enabled and alert on anomalies.");
  if (proposed.encryption === "Disabled") recommendations.push("Do not disable encryption for sensitive data.");
  if (proposed.exposure === "Internet") recommendations.push("Use WAF, rate limiting, strong authentication and continuous monitoring.");
  if (!recommendations.length) recommendations.push("No material increase was detected for the submitted controls.");
  return {
    currentScore, projectedScore, delta: projectedScore - currentScore,
    currentSeverity: severity(currentScore), severity: severity(projectedScore), factors, recommendations
  };
}

export const factorOptions = FACTORS.map(f => ({ key: f.key, label: f.label, values: Object.keys(f.values) }));
