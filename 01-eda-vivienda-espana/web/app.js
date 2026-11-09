(function () {
  "use strict";

  const KIND_LABELS = { total: "Total", nueva: "Nueva", usada: "Usada" };
  const SURFACES = [70, 90, 100];
  const NATIONAL_YEAR_DEFAULT = 2024;

  function groupNumber(value, digits, trim = false) {
    let fixed = Math.abs(value).toFixed(digits);
    if (trim && fixed.includes(".")) {
      fixed = fixed.replace(/\.?0+$/, "");
    }
    const [integer, fraction] = fixed.split(".");
    const grouped = integer.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    const sign = value < 0 && Number(fixed) !== 0 ? "−" : "";
    return `${sign}${grouped}${fraction ? `,${fraction}` : ""}`;
  }

  function parseLocaleNumber(raw) {
    let text = String(raw).replace(/[^\d.,-]/g, "").trim();
    if (!text) return null;
    const negative = text.startsWith("-");
    text = text.replace(/-/g, "");
    if (!text) return null;

    let normalized;
    if (text.includes(",")) {
      normalized = text.replace(/\./g, "").replace(",", ".");
    } else if (/^\d{1,3}(\.\d{3})+$/.test(text)) {
      normalized = text.replace(/\./g, "");
    } else {
      normalized = text;
    }

    const value = Number(normalized);
    if (!Number.isFinite(value)) return null;
    return negative ? -value : value;
  }

  const fmtEuro0 = { format: (value) => `${groupNumber(value, 0)} €` };
  const fmtNum0 = { format: (value) => groupNumber(value, 0) };
  const fmtNum1 = { format: (value) => groupNumber(value, 1, true) };
  const fmtNum2 = { format: (value) => groupNumber(value, 2) };

  const $ = (id) => document.getElementById(id);

  const els = {
    refYear: $("ref-year"),
    refYears: $("ref-years"),
    refPrice: $("ref-price"),
    refAbove: $("ref-above"),
    province: $("province"),
    year: $("year"),
    coverage: $("coverage-note"),
    reset: $("reset"),
    priceRange: $("price-range"),
    priceNumber: $("price"),
    incomeRange: $("income-range"),
    incomeNumber: $("income"),
    mortgageInputs: $("mortgage-inputs"),
    downRange: $("down-range"),
    downNumber: $("down"),
    rateRange: $("rate-range"),
    rateNumber: $("rate"),
    termRange: $("term-range"),
    termNumber: $("term"),
    resultYears: $("result-years"),
    resultMortgage: $("result-mortgage"),
    yearsValue: $("years-value"),
    yearsCaption: $("years-caption"),
    yearsPrice: $("years-price"),
    yearsIncome: $("years-income"),
    yearsPpm: $("years-ppm"),
    yearsMonthly: $("years-monthly"),
    rankYears: $("rank-years"),
    refLineYears: $("ref-line-years"),
    mortgageValue: $("mortgage-value"),
    mortgageCaption: $("mortgage-caption"),
    mortgageShare: $("mortgage-share"),
    shareFill: $("share-fill"),
    shareNote: $("share-note"),
    mortgageLoan: $("mortgage-loan"),
    mortgageDown: $("mortgage-down"),
    mortgageInterest: $("mortgage-interest"),
    mortgageCost: $("mortgage-cost"),
    rankMortgage: $("rank-mortgage"),
    refLineMortgage: $("ref-line-mortgage"),
    live: $("live"),
  };

  const state = {
    mode: "years",
    province: "00",
    year: NATIONAL_YEAR_DEFAULT,
    kind: "total",
    m2: 90,
    price: null,
    income: null,
    editedPrice: false,
    editedIncome: false,
    editedMortgage: false,
    down: 20,
    rate: 3,
    term: 25,
  };

  let data = null;
  let records = null;
  let provinceByCode = null;
  let urlTimer = null;

  init();

  async function init() {
    bindEvents();
    try {
      const response = await fetch("data/panel.json", { cache: "no-cache" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      data = await response.json();
      buildIndexes();
      buildProvinceSelect();
      readStateFromUrl();
      refresh(false);
      updateReferenceFigures();
      document.body.dataset.ready = "true";
    } catch (error) {
      showLoadError(error);
    }
  }

  function key(province, year, kind) {
    return `${province}|${year}|${kind}`;
  }

  function buildIndexes() {
    records = new Map();
    for (const row of data.records) {
      records.set(key(row.province_code, row.year, row.kind), row);
    }
    provinceByCode = new Map(data.provinces.map((province) => [province.code, province]));
  }

  function getRecord(province, year, kind) {
    if (year == null) return null;
    return records.get(key(province, year, kind)) || null;
  }

  function buildProvinceSelect() {
    const national = data.meta.national_code;
    const spain = data.provinces.filter((province) => province.code === national);
    const provinces = data.provinces.filter((province) => province.code !== national);

    els.province.replaceChildren();

    for (const province of spain) {
      els.province.append(new Option(province.name, province.code));
    }

    const provinceGroup = document.createElement("optgroup");
    provinceGroup.label = "Provincias";
    for (const province of provinces) {
      provinceGroup.append(new Option(province.name, province.code));
    }

    els.province.append(provinceGroup);
  }

  function readStateFromUrl() {
    const params = new URLSearchParams(window.location.search);

    const province = params.get("provincia");
    if (province && provinceByCode.has(province)) state.province = province;

    const kind = params.get("tipo");
    if (kind && KIND_LABELS[kind]) state.kind = kind;

    const m2 = Number(params.get("m2"));
    if (SURFACES.includes(m2)) state.m2 = m2;

    const mode = params.get("modo");
    if (mode === "hipoteca" || mode === "mortgage") state.mode = "mortgage";

    const year = Number(params.get("anio"));
    if (Number.isInteger(year)) state.year = year;

    const price = parseNumberParam(params.get("precio"));
    if (price != null && price >= 0) {
      state.price = price;
      state.editedPrice = true;
    }

    const income = parseNumberParam(params.get("renta"));
    if (income != null && income >= 0) {
      state.income = income;
      state.editedIncome = true;
    }

    const down = parseNumberParam(params.get("entrada"));
    if (down != null) {
      state.down = clamp(down, 0, 100);
      state.editedMortgage = true;
    }

    const rate = parseNumberParam(params.get("interes"));
    if (rate != null) {
      state.rate = clamp(rate, 0, 20);
      state.editedMortgage = true;
    }

    const term = parseNumberParam(params.get("plazo"));
    if (term != null) {
      state.term = clamp(term, 1, 50);
      state.editedMortgage = true;
    }
  }

  function parseNumberParam(value) {
    if (value == null || value === "") return null;
    const number = Number(value);
    return Number.isFinite(number) ? number : null;
  }

  function refresh(announce) {
    if (!data) return;
    syncYearOptions();
    loadPanelValues();
    syncControls();
    render(announce);
    writeUrl();
  }

  function availableYears(province, kind) {
    const years = [];
    for (let year = data.meta.end_year; year >= data.meta.start_year; year -= 1) {
      const row = getRecord(province, year, kind);
      if (row && row.price_eur_m2 != null && row.income_eur != null) {
        years.push(year);
      }
    }
    return years;
  }

  function syncYearOptions() {
    const years = availableYears(state.province, state.kind);

    if (!years.length) {
      els.year.replaceChildren();
      els.year.disabled = true;
      state.year = null;
      return;
    }

    els.year.disabled = false;
    if (!years.includes(state.year)) state.year = years[0];

    els.year.replaceChildren();
    for (const year of years) {
      els.year.append(new Option(String(year), String(year)));
    }
    els.year.value = String(state.year);
  }

  function loadPanelValues() {
    const row = getRecord(state.province, state.year, state.kind);
    if (!state.editedPrice) {
      state.price = row && row.price_eur_m2 != null ? row.price_eur_m2 : null;
    }
    if (!state.editedIncome) {
      state.income = row && row.income_eur != null ? row.income_eur : null;
    }
  }

  function syncControls() {
    els.province.value = state.province;
    els.year.value = state.year == null ? "" : String(state.year);

    const coverage = coverageNote(state.province, state.kind);
    els.coverage.textContent = coverage;
    els.coverage.hidden = !coverage;

    setRadio("kind", state.kind);
    setRadio("surface", String(state.m2));
    setRadio("mode", state.mode);

    const isNational = state.province === data.meta.national_code;
    $("key-spain-years").hidden = isNational;
    $("key-spain-mortgage").hidden = isNational;

    els.mortgageInputs.hidden = state.mode !== "mortgage";
    els.resultYears.hidden = state.mode !== "years";
    els.resultMortgage.hidden = state.mode !== "mortgage";

    syncNumber(els.priceNumber, state.price, 2, true);
    syncRange(els.priceRange, state.price, 300, 5000);
    syncNumber(els.incomeNumber, state.income, 0);
    syncRange(els.incomeRange, state.income, 0, 100000);
    syncNumber(els.downNumber, state.down, 0);
    syncRange(els.downRange, state.down, 0, 100);
    syncNumber(els.rateNumber, state.rate, 2, true);
    syncRange(els.rateRange, state.rate, 0, 8);
    syncNumber(els.termNumber, state.term, 0);
    syncRange(els.termRange, state.term, 5, 40);

    els.reset.disabled = !(state.editedPrice || state.editedIncome || state.editedMortgage);
  }

  function setRadio(name, value) {
    document.querySelectorAll(`input[name="${name}"]`).forEach((input) => {
      input.checked = input.value === value;
    });
  }

  function syncNumber(input, value, digits, trim = false, force = false) {
    if (!force && document.activeElement === input) return;
    input.value =
      value == null || !Number.isFinite(value) ? "" : groupNumber(value, digits, trim);
  }

  function syncRange(range, value, min, max) {
    if (document.activeElement === range) return;
    range.value = String(value == null ? min : clamp(value, min, max));
  }

  function coverageNote(province, kind) {
    let incomeStart = null;
    const missingPrice = [];

    for (let year = data.meta.start_year; year <= data.meta.end_year; year += 1) {
      const row = getRecord(province, year, kind);
      if (row && row.income_eur != null && incomeStart == null) {
        incomeStart = year;
      }
      if (!row || row.price_eur_m2 == null) {
        missingPrice.push(year);
      }
    }

    const parts = [];
    if (incomeStart == null) {
      parts.push("Sin datos de renta");
    } else if (incomeStart > data.meta.start_year) {
      parts.push(`Renta desde ${incomeStart}`);
    }
    if (missingPrice.length) {
      parts.push(`Sin precio en ${formatYearRanges(missingPrice)}`);
    }

    return parts.join(" · ");
  }

  function formatYearRanges(years) {
    if (!years.length) return "";
    const sorted = [...new Set(years)].sort((a, b) => a - b);
    const ranges = [];
    let start = sorted[0];
    let previous = sorted[0];

    for (let index = 1; index < sorted.length; index += 1) {
      const year = sorted[index];
      if (year === previous + 1) {
        previous = year;
        continue;
      }
      ranges.push(start === previous ? `${start}` : `${start}–${previous}`);
      start = year;
      previous = year;
    }
    ranges.push(start === previous ? `${start}` : `${start}–${previous}`);
    return ranges.join(", ");
  }

  function provinceName(code) {
    const province = provinceByCode.get(code);
    return province ? province.name : code;
  }

  function renderYears() {
    const price = Calc.priceFor(state.price, state.m2);
    const years = Calc.yearsFor(price, state.income);
    const province = provinceName(state.province);

    if (price == null || years == null) {
      els.yearsValue.textContent = "—";
      els.yearsCaption.textContent =
        state.price == null
          ? "No hay precio para este año y tipo de vivienda."
          : "Añade una renta mayor que cero para calcular los años.";
      els.yearsPrice.textContent = price == null ? "—" : fmtEuro0.format(price);
      els.yearsIncome.textContent = state.income == null ? "—" : fmtEuro0.format(state.income);
      els.yearsPpm.textContent = state.price == null ? "—" : `${fmtNum2.format(state.price)} €/m²`;
      els.yearsMonthly.textContent =
        state.income == null ? "—" : `${fmtEuro0.format(state.income / 12)}/mes`;
      clearDistribution("years");
      els.rankYears.textContent = "";
      els.refLineYears.textContent = "";
      return;
    }

    els.yearsValue.textContent = fmtNum2.format(years);
    els.yearsCaption.textContent =
      `Una vivienda de ${state.m2} m² en ${province} (${state.year}), ` +
      "pagada con la renta anual del hogar.";
    els.yearsPrice.textContent = fmtEuro0.format(price);
    els.yearsIncome.textContent = fmtEuro0.format(state.income);
    els.yearsPpm.textContent = `${fmtNum2.format(state.price)} €/m²`;
    els.yearsMonthly.textContent = `${fmtEuro0.format(state.income / 12)}/mes`;

    const nationalCode = data.meta.national_code;
    const provinces = data.provinces.filter((province) => province.code !== nationalCode);
    const series = [];

    for (const item of provinces) {
      const row = getRecord(item.code, state.year, state.kind);
      if (!row || row.price_eur_m2 == null || row.income_eur == null) continue;
      const value = Calc.yearsFor(row.price_eur_m2 * state.m2, row.income_eur);
      if (value != null) {
        series.push({ code: item.code, name: item.name, value });
      }
    }

    const nationalRow = getRecord(nationalCode, state.year, state.kind);
    const spainValue =
      nationalRow && nationalRow.price_eur_m2 != null && nationalRow.income_eur != null
        ? Calc.yearsFor(nationalRow.price_eur_m2 * state.m2, nationalRow.income_eur)
        : null;
    const median = Calc.median(series.map((item) => item.value));

    drawDistribution("years", series, years, spainValue, {
      cap: 50,
      stepFor: (rawMax) => (rawMax <= 12 ? 2 : rawMax <= 30 ? 5 : 10),
      minMax: 8,
      threshold: null,
      format: (value) => `${fmtNum2.format(value)} años`,
      axisLabel: (value) => fmtNum0.format(value),
      capNote: "El eje se corta en 50 años; tu caso queda fuera de escala.",
    });

    if (series.length) {
      const below = series.filter((item) => item.value < years).length;
      let text =
        below === 0
          ? "No hay ninguna provincia por debajo."
          : `Está por encima de ${below} de las ${series.length} provincias.`;
      if (spainValue != null && state.province !== nationalCode) {
        const difference = years - spainValue;
        if (Math.abs(difference) < 0.005) {
          text += " Igual que la referencia de España.";
        } else {
          text +=
            ` ${fmtNum2.format(Math.abs(difference))} años ` +
            `${difference > 0 ? "más" : "menos"} que España.`;
        }
      }
      els.rankYears.textContent = text;
    } else {
      els.rankYears.textContent = "";
    }

    const references = [];
    if (spainValue != null && state.province !== nationalCode) {
      references.push(`España ${state.year}: ${fmtNum2.format(spainValue)} años`);
    }
    if (median != null) {
      references.push(`Mediana provincial: ${fmtNum2.format(median)} años`);
    }
    els.refLineYears.textContent = references.join(" · ");
  }

  function renderMortgage() {
    const price = Calc.priceFor(state.price, state.m2);
    const mortgage = Calc.mortgageFor(price, state.down, state.rate, state.term);

    if (!mortgage) {
      els.mortgageValue.textContent = "—";
      els.mortgageCaption.textContent =
        state.price == null
          ? "No hay precio para este año y tipo de vivienda."
          : "Revisa los supuestos de la hipoteca.";
      clearMortgageStats();
      clearShare();
      clearDistribution("mortgage");
      els.rankMortgage.textContent = "";
      els.refLineMortgage.textContent = "";
      return;
    }

    const share = Calc.incomeShare(mortgage.payment, state.income);

    els.mortgageValue.textContent = fmtEuro0.format(mortgage.payment);
    els.mortgageCaption.textContent =
      `Hipoteca fija a ${fmtNum1.format(state.term)} años, ` +
      `${fmtNum1.format(state.down)} % de entrada y ${fmtNum2.format(state.rate)} % de interés.`;
    els.mortgageLoan.textContent = fmtEuro0.format(mortgage.principal);
    els.mortgageDown.textContent = fmtEuro0.format(mortgage.down);
    els.mortgageInterest.textContent = fmtEuro0.format(mortgage.totalInterest);
    els.mortgageCost.textContent = fmtEuro0.format(mortgage.totalCost);

    if (share == null) {
      clearShare();
    } else {
      renderShare(share);
    }

    if (share == null) {
      clearDistribution("mortgage");
      els.rankMortgage.textContent = "";
      els.refLineMortgage.textContent = "";
      return;
    }

    const nationalCode = data.meta.national_code;
    const provinces = data.provinces.filter((province) => province.code !== nationalCode);
    const series = [];

    for (const item of provinces) {
      const row = getRecord(item.code, state.year, state.kind);
      if (!row || row.price_eur_m2 == null || row.income_eur == null) continue;
      const provinceMortgage = Calc.mortgageFor(
        row.price_eur_m2 * state.m2,
        state.down,
        state.rate,
        state.term
      );
      const value = provinceMortgage
        ? Calc.incomeShare(provinceMortgage.payment, row.income_eur)
        : null;
      if (value != null) {
        series.push({ code: item.code, name: item.name, value });
      }
    }

    const nationalRow = getRecord(nationalCode, state.year, state.kind);
    const spainShare =
      nationalRow && nationalRow.price_eur_m2 != null && nationalRow.income_eur != null
        ? (() => {
            const nationalMortgage = Calc.mortgageFor(
              nationalRow.price_eur_m2 * state.m2,
              state.down,
              state.rate,
              state.term
            );
            return nationalMortgage
              ? Calc.incomeShare(nationalMortgage.payment, nationalRow.income_eur)
              : null;
          })()
        : null;
    const median = Calc.median(series.map((item) => item.value));

    drawDistribution("mortgage", series, share, spainShare, {
      cap: 200,
      stepFor: (rawMax) => (rawMax <= 80 ? 10 : rawMax <= 150 ? 20 : 50),
      minMax: 60,
      threshold: 30,
      format: (value) => `${fmtNum1.format(value)} % de la renta mensual`,
      axisLabel: (value) => `${fmtNum0.format(value)} %`,
      capNote: "El eje se corta en 200 %; tu caso queda fuera de escala.",
    });

    if (series.length) {
      const below = series.filter((item) => item.value < share).length;
      let text =
        below === 0
          ? "No hay ninguna provincia por debajo."
          : `Está por encima de ${below} de las ${series.length} provincias.`;
      if (spainShare != null && state.province !== nationalCode) {
        const difference = share - spainShare;
        if (Math.abs(difference) < 0.05) {
          text += " Igual que la referencia de España.";
        } else {
          text +=
            ` ${fmtNum1.format(Math.abs(difference))} puntos ` +
            `${difference > 0 ? "más" : "menos"} que España.`;
        }
      }
      els.rankMortgage.textContent = text;
    } else {
      els.rankMortgage.textContent = "";
    }

    const references = [];
    if (spainShare != null && state.province !== nationalCode) {
      references.push(
        `España ${state.year}: ${fmtNum1.format(spainShare)} % de la renta mensual`
      );
    }
    if (median != null) {
      references.push(`Mediana provincial: ${fmtNum1.format(median)} %`);
    }
    els.refLineMortgage.textContent = references.join(" · ");
  }

  function renderShare(share) {
    const level = share <= 30 ? "is-low" : share <= 40 ? "is-mid" : "is-high";
    els.mortgageShare.textContent = `${fmtNum1.format(share)} %`;
    els.mortgageShare.className = `share-value ${level}`;
    els.shareFill.className = `share-fill ${level}`;
    els.shareFill.style.width = `${Math.min(100, share)}%`;

    if (share <= 30) {
      els.shareNote.textContent = "Por debajo de la referencia orientativa del 30 %.";
    } else if (share <= 40) {
      els.shareNote.textContent = "Entre el 30 % y el 40 % de la renta mensual.";
    } else {
      els.shareNote.textContent = "Por encima del 40 % de la renta mensual.";
    }
  }

  function clearShare() {
    els.mortgageShare.textContent = "—";
    els.mortgageShare.className = "share-value";
    els.shareFill.className = "share-fill";
    els.shareFill.style.width = "0%";
    els.shareNote.textContent = "Añade una renta mayor que cero para calcular el porcentaje.";
  }

  function clearMortgageStats() {
    els.mortgageLoan.textContent = "—";
    els.mortgageDown.textContent = "—";
    els.mortgageInterest.textContent = "—";
    els.mortgageCost.textContent = "—";
  }

  function drawDistribution(prefix, series, selected, reference, options) {
    const rug = $(`rug-${prefix}`);
    const spain = $(`spain-${prefix}`);
    const you = $(`you-${prefix}`);
    const axis = $(`axis-${prefix}`);
    const note = $(`dist-note-${prefix}`);
    const container = $(`dist-${prefix}`);
    const threshold = prefix === "mortgage" ? $("threshold-mortgage") : null;

    const values = series.map((item) => item.value).filter(Number.isFinite);
    const observed = Math.max(0, selected ?? 0, reference ?? 0, ...values);
    const capped = observed > options.cap;
    const bounded = Math.min(observed, options.cap);
    const rawMax = Math.max(options.minMax, capped ? bounded : bounded * 1.04);
    const step = options.stepFor(rawMax);
    const max = Math.ceil(rawMax / step) * step;
    const percent = (value) => Math.max(0, Math.min(100, (value / max) * 100));

    rug.replaceChildren();
    for (const value of values) {
      const tick = document.createElement("span");
      tick.style.left = `${percent(value)}%`;
      rug.append(tick);
    }

    spain.hidden = reference == null;
    if (reference != null) spain.style.left = `${percent(reference)}%`;

    you.hidden = selected == null;
    if (selected != null) you.style.left = `${percent(selected)}%`;

    if (threshold != null) {
      const hasThreshold = options.threshold != null;
      threshold.hidden = !hasThreshold;
      if (hasThreshold) threshold.style.left = `${percent(options.threshold)}%`;
    }

    axis.replaceChildren();
    for (let tick = 0; tick <= max + 1e-9; tick += step) {
      const label = document.createElement("span");
      label.textContent = options.axisLabel(tick);
      label.style.left = `${percent(tick)}%`;
      axis.append(label);
    }

    note.hidden = !capped;
    note.textContent = capped ? options.capNote : "";

    const aria = [];
    if (selected != null) aria.push(`Tu caso: ${options.format(selected)}.`);
    if (reference != null) aria.push(`España: ${options.format(reference)}.`);
    if (options.threshold != null) aria.push("Referencia orientativa del 30 %.");
    aria.push(`${series.length} provincias.`);
    container.setAttribute("aria-label", aria.join(" "));
  }

  function clearDistribution(prefix) {
    const rug = $(`rug-${prefix}`);
    const spain = $(`spain-${prefix}`);
    const you = $(`you-${prefix}`);
    const axis = $(`axis-${prefix}`);
    const note = $(`dist-note-${prefix}`);
    const container = $(`dist-${prefix}`);
    const threshold = prefix === "mortgage" ? $("threshold-mortgage") : null;

    rug.replaceChildren();
    spain.hidden = true;
    you.hidden = true;
    if (threshold != null) threshold.hidden = true;
    axis.replaceChildren();
    note.hidden = true;
    note.textContent = "";
    container.setAttribute("aria-label", "Sin datos para dibujar la distribución.");
  }

  function render(announce) {
    if (!data) return;
    renderYears();
    renderMortgage();
    if (announce) announceResult();
  }

  function announceResult() {
    let message;

    if (state.mode === "years") {
      const price = Calc.priceFor(state.price, state.m2);
      const years = Calc.yearsFor(price, state.income);
      message =
        years == null
          ? "Sin resultado para los valores actuales."
          : `${fmtNum2.format(years)} años de renta para una vivienda de ` +
            `${state.m2} metros cuadrados en ${provinceName(state.province)}.`;
    } else {
      const price = Calc.priceFor(state.price, state.m2);
      const mortgage = Calc.mortgageFor(price, state.down, state.rate, state.term);
      const share = mortgage ? Calc.incomeShare(mortgage.payment, state.income) : null;
      message =
        mortgage == null
          ? "Sin resultado para los valores actuales."
          : `Cuota de ${fmtEuro0.format(mortgage.payment)} al mes` +
            (share == null ? "." : `, ${fmtNum1.format(share)} por ciento de la renta mensual.`);
    }

    els.live.textContent = message;
  }

  function updateReferenceFigures() {
    const year = data.meta.end_year;
    const m2 = data.meta.reference_m2;
    const nationalCode = data.meta.national_code;

    els.refYear.textContent = String(year);

    const nationalRow = getRecord(nationalCode, year, "total");
    const spainYears =
      nationalRow && nationalRow.price_eur_m2 != null && nationalRow.income_eur != null
        ? Calc.yearsFor(nationalRow.price_eur_m2 * m2, nationalRow.income_eur)
        : null;
    const spainPrice = nationalRow && nationalRow.price_eur_m2 != null
      ? nationalRow.price_eur_m2 * m2
      : null;

    const provinces = data.provinces.filter((province) => province.code !== nationalCode);
    const prices = [];

    for (const province of provinces) {
      const row = getRecord(province.code, year, "total");
      if (!row || row.price_eur_m2 == null) continue;
      prices.push(row.price_eur_m2 * m2);
    }

    const medianPrice = Calc.median(prices);
    const above = spainPrice == null ? null : prices.filter((price) => price > spainPrice).length;

    els.refYears.textContent = spainYears == null ? "—" : `${fmtNum2.format(spainYears)} años`;
    els.refPrice.textContent = medianPrice == null ? "—" : fmtEuro0.format(medianPrice);
    els.refAbove.textContent = above == null ? "—" : `${above} de ${prices.length}`;
  }

  function bindEvents() {
    const form = $("controls");
    form.addEventListener("submit", (event) => event.preventDefault());

    els.province.addEventListener("change", () => {
      state.province = els.province.value;
      resetEdits();
      refresh(true);
    });

    els.year.addEventListener("change", () => {
      const year = Number(els.year.value);
      if (Number.isInteger(year)) {
        state.year = year;
        resetEdits();
        refresh(true);
      }
    });

    document.querySelectorAll('input[name="kind"]').forEach((input) => {
      input.addEventListener("change", () => {
        if (!input.checked) return;
        state.kind = input.value;
        resetEdits();
        refresh(true);
      });
    });

    document.querySelectorAll('input[name="surface"]').forEach((input) => {
      input.addEventListener("change", () => {
        if (!input.checked) return;
        state.m2 = Number(input.value);
        refresh(true);
      });
    });

    document.querySelectorAll('input[name="mode"]').forEach((input) => {
      input.addEventListener("change", () => {
        if (!input.checked) return;
        state.mode = input.value;
        refresh(true);
      });
    });

    bindPair(els.priceRange, els.priceNumber, "price", {
      min: 0,
      max: 20000,
      digits: 2,
      trim: true,
      editedKey: "editedPrice",
    });
    bindPair(els.incomeRange, els.incomeNumber, "income", {
      min: 0,
      max: 500000,
      digits: 0,
      editedKey: "editedIncome",
    });
    bindPair(els.downRange, els.downNumber, "down", {
      min: 0,
      max: 100,
      digits: 0,
      mortgage: true,
    });
    bindPair(els.rateRange, els.rateNumber, "rate", {
      min: 0,
      max: 20,
      digits: 2,
      trim: true,
      mortgage: true,
    });
    bindPair(els.termRange, els.termNumber, "term", {
      min: 1,
      max: 50,
      digits: 0,
      mortgage: true,
    });

    els.reset.addEventListener("click", () => {
      resetEdits();
      state.down = 20;
      state.rate = 3;
      state.term = 25;
      state.editedMortgage = false;
      refresh(true);
    });
  }

  function bindPair(range, number, property, options) {
    range.addEventListener("input", () => {
      state[property] = Number(range.value);
      if (options.editedKey) state[options.editedKey] = true;
      if (options.mortgage) state.editedMortgage = true;
      refresh(false);
    });

    number.addEventListener("input", () => {
      const parsed = parseLocaleNumber(number.value);
      if (parsed != null) {
        state[property] = parsed;
      } else if (!number.value.trim()) {
        state[property] = null;
      }
      if (options.editedKey) state[options.editedKey] = true;
      if (options.mortgage) state.editedMortgage = true;
      refresh(false);
    });

    number.addEventListener("change", () => {
      const parsed = parseLocaleNumber(number.value);
      const clamped =
        parsed == null ? options.min : clamp(parsed, options.min, options.max);
      const step = options.digits === 2 ? 0.01 : 1;
      state[property] = Math.round(clamped / step) * step;
      if (options.editedKey) state[options.editedKey] = true;
      if (options.mortgage) state.editedMortgage = true;
      refresh(true);
      syncNumber(number, state[property], options.digits, options.trim, true);
    });
  }

  function resetEdits() {
    state.editedPrice = false;
    state.editedIncome = false;
  }

  function writeUrl() {
    window.clearTimeout(urlTimer);
    urlTimer = window.setTimeout(() => {
      const params = new URLSearchParams();

      if (state.province !== data.meta.national_code) {
        params.set("provincia", state.province);
      }
      if (state.year != null && state.year !== data.meta.end_year) {
        params.set("anio", String(state.year));
      }
      if (state.kind !== "total") params.set("tipo", state.kind);
      if (state.m2 !== 90) params.set("m2", String(state.m2));
      if (state.mode === "mortgage") {
        params.set("modo", "hipoteca");
        if (state.down !== 20) params.set("entrada", trimNumber(state.down));
        if (state.rate !== 3) params.set("interes", trimNumber(state.rate));
        if (state.term !== 25) params.set("plazo", trimNumber(state.term));
      }
      if (state.editedPrice && state.price != null) {
        params.set("precio", trimNumber(state.price));
      }
      if (state.editedIncome && state.income != null) {
        params.set("renta", trimNumber(state.income));
      }

      const query = params.toString();
      const url = `${window.location.pathname}${query ? `?${query}` : ""}`;
      window.history.replaceState(null, "", url);
    }, 120);
  }

  function trimNumber(value) {
    return String(Number(value.toFixed(4)));
  }

  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  function showLoadError() {
    document.body.dataset.ready = "error";
    const message =
      "No se han podido cargar los datos. Abre la página con un servidor local: " +
      "python -m http.server 8000 y entra en http://localhost:8000/web/.";
    els.yearsCaption.textContent = message;
    els.mortgageCaption.textContent = message;
    els.yearsValue.textContent = "—";
    els.mortgageValue.textContent = "—";
    els.province.disabled = true;
    els.year.disabled = true;
    els.reset.disabled = true;
  }
})();
