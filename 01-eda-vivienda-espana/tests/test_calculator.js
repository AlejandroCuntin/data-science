/*
 * Comprobaciones de la calculadora y del JSON que consume.
 * Uso: node tests/test_calculator.js
 */

const assert = require("node:assert/strict");
const Calc = require("../web/calc.js");
const data = require("../web/data/panel.json");

const records = new Map(
  data.records.map((row) => [`${row.province_code}|${row.year}|${row.kind}`, row])
);

function record(province, year, kind) {
  return records.get(`${province}|${year}|${kind}`);
}

function close(actual, expected, tolerance, label) {
  assert.ok(
    Math.abs(actual - expected) <= tolerance,
    `${label}: esperado ${expected}, obtenido ${actual}`
  );
}

// Estructura del export
assert.equal(data.provinces.length, 53, "52 provincias + España");
assert.equal(data.records.length, 1590, "53 territorios × 10 años × 3 tipos");
assert.equal(data.meta.start_year, 2015);
assert.equal(data.meta.end_year, 2024);
assert.ok(data.records.every((row) => row.year >= 2015 && row.year <= 2024));
assert.equal(
  data.records.filter((row) => row.price_eur_m2 === null).length,
  27,
  "huecos de precio en nueva"
);
assert.equal(
  data.records.filter((row) => row.income_eur === null).length,
  54,
  "huecos de renta declarados"
);
assert.equal(record("00", 2015, "total").income_eur, null, "la renta nacional empieza en 2021");
assert.equal(record("42", 2017, "nueva").price_eur_m2, null, "Soria no tiene precio de nueva en 2017");
assert.equal(record("28", 2024, "total").price_eur_m2, 3239.95);
assert.equal(record("28", 2024, "total").income_eur, 51928);
assert.equal(record("13", 2024, "total").price_eur_m2, 721.68);
assert.equal(record("13", 2024, "total").income_eur, 33136);
assert.equal(record("00", 2024, "total").price_eur_m2, 1913.62);
assert.equal(record("00", 2024, "total").income_eur, 40605);

// Años de renta: los tres casos del notebook.
const madridPrice = Calc.priceFor(record("28", 2024, "total").price_eur_m2, 90);
const madridYears = Calc.yearsFor(madridPrice, record("28", 2024, "total").income_eur);
close(madridPrice, 291595.5, 0.01, "precio Madrid 90 m²");
close(madridYears, 5.6154, 0.0001, "años Madrid");

const ciudadRealPrice = Calc.priceFor(record("13", 2024, "total").price_eur_m2, 90);
const ciudadRealYears = Calc.yearsFor(
  ciudadRealPrice,
  record("13", 2024, "total").income_eur
);
close(ciudadRealPrice, 64951.2, 0.01, "precio Ciudad Real 90 m²");
close(ciudadRealYears, 1.9601, 0.0001, "años Ciudad Real");

const spainPrice = Calc.priceFor(record("00", 2024, "total").price_eur_m2, 90);
const spainYears = Calc.yearsFor(spainPrice, record("00", 2024, "total").income_eur);
close(spainPrice, 172225.8, 0.01, "precio España 90 m²");
close(spainYears, 4.2415, 0.0001, "años España");

// Hipoteca: Madrid, 20 % de entrada, 3 % y 25 años.
const mortgage = Calc.mortgageFor(madridPrice, 20, 3, 25);
close(mortgage.down, 58319.1, 0.01, "entrada Madrid");
close(mortgage.principal, 233276.4, 0.01, "préstamo Madrid");
close(mortgage.payment, 1106.2, 0.1, "cuota Madrid");
close(mortgage.months, 300, 0, "meses Madrid");

const share = Calc.incomeShare(mortgage.payment, record("28", 2024, "total").income_eur);
close(share, 25.56, 0.01, "porcentaje de renta Madrid");

// Casos límite.
const zeroRate = Calc.mortgageFor(100000, 20, 0, 25);
close(zeroRate.payment, 80000 / 300, 0.0001, "tipo 0 %");
close(zeroRate.totalInterest, 0, 0.0001, "intereses con tipo 0 %");

const fullDown = Calc.mortgageFor(100000, 100, 3, 25);
close(fullDown.payment, 0, 0, "entrada del 100 %");
close(fullDown.principal, 0, 0, "préstamo con entrada del 100 %");
close(fullDown.totalCost, 100000, 0.0001, "coste con entrada del 100 %");

assert.equal(Calc.incomeShare(1000, 0), null, "sin renta no hay porcentaje");
assert.equal(Calc.yearsFor(100000, 0), null, "sin renta no hay años");
assert.equal(Calc.priceFor(null, 90), null, "sin precio no hay coste");
assert.equal(Calc.median([1, 2, 3, 4]), 2.5, "mediana par");
assert.equal(Calc.median([1, 2, 3]), 2, "mediana impar");
assert.equal(Calc.median([]), null, "mediana vacía");

console.log("OK · calculadora y export coherentes");
console.log(
  `Madrid 2024: ${madridYears.toFixed(2)} años · ` +
    `${Math.round(madridPrice).toLocaleString("es-ES")} € · ` +
    `${Math.round(mortgage.payment).toLocaleString("es-ES")} €/mes · ` +
    `${share.toFixed(1)} % de la renta`
);
console.log(
  `Ciudad Real 2024: ${ciudadRealYears.toFixed(2)} años · ` +
    `${Math.round(ciudadRealPrice).toLocaleString("es-ES")} €`
);
console.log(
  `España 2024: ${spainYears.toFixed(2)} años · ` +
    `${Math.round(spainPrice).toLocaleString("es-ES")} €`
);
