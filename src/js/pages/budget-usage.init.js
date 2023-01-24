data = document.getElementById('budget-data').getAttribute('data-budget-usage')
json_data = JSON.parse(data)
// get colors array from the string
function getChartColorsArray(chartId) {
    if (document.getElementById(chartId) !== null) {
        var colors = document.getElementById(chartId).getAttribute("data-colors");
        if (colors) {
            colors = JSON.parse(colors);
            return colors.map(function (value) {
                var newValue = value.replace(" ", "");
                if (newValue.indexOf(",") === -1) {
                    var color = getComputedStyle(document.documentElement).getPropertyValue(
                        newValue
                    );
                    if (color) return color;
                    else return newValue;
                } else {
                    var val = value.split(",");
                    if (val.length == 2) {
                        var rgbaColor = getComputedStyle(
                            document.documentElement
                        ).getPropertyValue(val[0]);
                        rgbaColor = "rgba(" + rgbaColor + "," + val[1] + ")";
                        return rgbaColor;
                    } else {
                        return newValue;
                    }
                }
            });
        } else {
            console.warn('data-colors atributes not found on', chartId);
        }
    }
}


if(json_data.length >= 1){
    Array.from(json_data).forEach(data => {
        var chartRadialbarBasicColors = getChartColorsArray("month-"+data.id);
        if (chartRadialbarBasicColors) {
        var options = {
            series: [Math.round((data.spent *100) / data.planed)],
            chart: {
                type: 'radialBar',
                width: 105,
                sparkline: {
                    enabled: true
                }
            },
            dataLabels: {
                enabled: false
            },
            plotOptions: {
                radialBar: {
                    hollow: {
                        margin: 0,
                        size: '70%'
                    },
                    track: {
                        margin: 1
                    },
                    dataLabels: {
                        show: true,
                        name: {
                            show: false
                        },
                        value: {
                            show: true,
                            fontSize: '16px',
                            fontWeight: 600,
                            offsetY: 8,
                        }
                    }
                }
            },
            colors: chartRadialbarBasicColors
        };

        var chart = new ApexCharts(document.querySelector("#month-"+data.id), options);
        chart.render();
}
    })

}

