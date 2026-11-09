/* Funciones puras de la calculadora. Sin DOM, para poder probarlas con Node. */
(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.Calc = factory();
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  function finite(value) {
    return typeof value === "number" && Number.isFinite(value);
  }

  function priceFor(pricePerM2, m2) {
    if (!finite(pricePerM2) || !finite(m2) || pricePerM2 < 0 || m2 <= 0) return null;
    return pricePerM2 * m2;
  }

  function yearsFor(price, annualIncome) {
    if (!finite(price) || !finite(annualIncome) || price < 0 || annualIncome <= 0) return null;
    return price / annualIncome;
  }

  function mortgageFor(price, downPercent, annualRate, termYears) {
    if (
      !finite(price) ||
      !finite(downPercent) ||
      !finite(annualRate) ||
      !finite(termYears) ||
      price < 0 ||
      downPercent < 0 ||
      downPercent > 100 ||
      annualRate < 0 ||
      termYears <= 0
    ) {
      return null;
    }

    const months = Math.round(termYears * 12);
    if (months <= 0) return null;

    const down = price * (downPercent / 100);
    const principal = Math.max(0, price - down);
    const monthlyRate = annualRate / 100 / 12;

    let payment;
    if (principal === 0) {
      payment = 0;
    } else if (monthlyRate === 0) {
      payment = principal / months;
    } else {
      const factor = Math.pow(1 + monthlyRate, -months);
      payment = (principal * monthlyRate) / (1 - factor);
    }

    const totalPaid = payment * months;
    const totalInterest = Math.max(0, totalPaid - principal);

    return {
      down,
      principal,
      months,
      payment,
      totalPaid,
      totalInterest,
      totalCost: down + totalPaid,
    };
  }

  function incomeShare(payment, annualIncome) {
    if (!finite(payment) || !finite(annualIncome) || payment < 0 || annualIncome <= 0) {
      return null;
    }
    return (payment / (annualIncome / 12)) * 100;
  }

  function median(values) {
    const clean = values.filter(finite).sort((a, b) => a - b);
    if (!clean.length) return null;
    const middle = Math.floor(clean.length / 2);
    return clean.length % 2
      ? clean[middle]
      : (clean[middle - 1] + clean[middle]) / 2;
  }

  return { priceFor, yearsFor, mortgageFor, incomeShare, median };
});
