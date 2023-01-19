
// get colors array from the string
function getChartColorsArray(chartId) {
    if (document.getElementById(chartId) !== null) {
        var colors = document.getElementById(chartId).getAttribute("data-colors");
        if (colors) {
            colors = JSON.parse(colors);
            return colors.map(function (value) {
                var newValue = value.replace(" ", "");
                if (newValue.indexOf(",") === -1) {
                    var color = getComputedStyle(document.documentElement).getPropertyValue(newValue);
                    if (color) return color;
                    else return newValue;;
                } else {
                    var val = value.split(',');
                    if (val.length == 2) {
                        var rgbaColor = getComputedStyle(document.documentElement).getPropertyValue(val[0]);
                        rgbaColor = "rgba(" + rgbaColor + "," + val[1] + ")";
                        return rgbaColor;
                    } else {
                        return newValue;
                    }
                }
            });
        } else {
            console.warn('data-colors Attribute not found on:', chartId);
        }
    }
}

// Balance Overview charts
var revenueExpensesCdfChartsColors = getChartColorsArray("revenue-expenses-cdf-charts");
if (revenueExpensesCdfChartsColors) {

    const xhttp = new XMLHttpRequest();
    xhttp.open('GET', '/tresorerie/balance/cdf')
    xhttp.send()
    xhttp.onload = function () {
      let json_records = JSON.parse(this.responseText);

        if(json_records.length > 0) {
            incomes = []
            outcomes = []
            budget_total = 0

            Array.from(json_records).forEach((data, index) => {
                budget_total += data.budget
                incomes.push(data.income)
                outcomes.push(data.outcome)
            });

            let options = {
                series: [{
                    name: 'Revenus',
                    data: incomes
                }, {
                    name: 'Dépenses',
                    data: outcomes
                }],
                chart: {
                    height: 290,
                    type: 'area',
                    toolbar: 'false',
                },
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    curve: 'smooth',
                    width: 2,
                },
                xaxis: {
                    categories: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aou', 'Sep', 'Oct', 'Nov', 'Déc']
                },
                yaxis: {
                    labels: {
                        formatter: function (value) {
                            return "cdf " + value;
                        }
                    },

                },
                colors: revenueExpensesCdfChartsColors,
                fill: {
                    opacity: 0.06,
                    colors: revenueExpensesCdfChartsColors,
                    type: 'solid'
                }
            };
            let chart = new ApexCharts(document.querySelector("#revenue-expenses-cdf-charts"), options);
            chart.render();
        }
    }
}

// Balance Overview charts
var revenueExpensesUsdChartsColors = getChartColorsArray("revenue-expenses-usd-charts");
if (revenueExpensesUsdChartsColors) {

    const xhttp = new XMLHttpRequest();
    xhttp.open('GET', '/tresorerie/balance/usd')
    xhttp.send()
    xhttp.onload = function () {
      let json_records = JSON.parse(this.responseText);

        if(json_records.length > 0) {
            incomes = []
            outcomes = []
            budget_total = 0

            Array.from(json_records).forEach((data, index) => {
                budget_total += data.budget
                incomes.push(data.income)
                outcomes.push(data.outcome)
            });

            let options = {
                series: [{
                    name: 'Revenus',
                    data: incomes
                }, {
                    name: 'Dépenses',
                    data: outcomes
                }],
                chart: {
                    height: 290,
                    type: 'area',
                    toolbar: 'false',
                },
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    curve: 'smooth',
                    width: 2,
                },
                xaxis: {
                    categories: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aou', 'Sep', 'Oct', 'Nov', 'Déc']
                },
                yaxis: {
                    labels: {
                        formatter: function (value) {
                            return "usd " + value;
                        }
                    },

                },
                colors: revenueExpensesCdfChartsColors,
                fill: {
                    opacity: 0.06,
                    colors: revenueExpensesCdfChartsColors,
                    type: 'solid'
                }
            };
            let chart = new ApexCharts(document.querySelector("#revenue-expenses-usd-charts"), options);
            chart.render();
        }
    }
}