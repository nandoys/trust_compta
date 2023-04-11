function getChartColorsArray(e){if(null!==document.getElementById(e)){var t=document.getElementById(e).getAttribute("data-colors");if(t)return(t=JSON.parse(t)).map(function(e){var t=e.replace(" ","");return-1===t.indexOf(",")?getComputedStyle(document.documentElement).getPropertyValue(t)||t:2==(e=e.split(",")).length?"rgba("+getComputedStyle(document.documentElement).getPropertyValue(e[0])+","+e[1]+")":t});console.warn("data-colors Attribute not found on:",e)}}var revenueExpensesCdfChartsColors=getChartColorsArray("revenue-expenses-cdf-charts");if(revenueExpensesCdfChartsColors){const h=new XMLHttpRequest;h.open("GET","/tresorerie/balance/cdf"),h.send(),h.onload=function(){var e=JSON.parse(this.responseText);0<e.length&&(incomes=[],outcomes=[],budget_total=0,Array.from(e).forEach((e,t)=>{budget_total+=e.budget,incomes.push(e.income),outcomes.push(e.outcome)}),e={series:[{name:"Revenus",data:incomes},{name:"Dépenses",data:outcomes}],chart:{height:290,type:"area",toolbar:"false"},dataLabels:{enabled:!1},stroke:{curve:"smooth",width:2},xaxis:{categories:["Jan","Fév","Mar","Avr","Mai","Juin","Juil","Aou","Sep","Oct","Nov","Déc"]},yaxis:{labels:{formatter:function(e){return"cdf "+e}}},colors:revenueExpensesCdfChartsColors,fill:{opacity:.06,colors:revenueExpensesCdfChartsColors,type:"solid"}},new ApexCharts(document.querySelector("#revenue-expenses-cdf-charts"),e).render())}}var revenueExpensesUsdChartsColors=getChartColorsArray("revenue-expenses-usd-charts");if(revenueExpensesUsdChartsColors){const o=new XMLHttpRequest;o.open("GET","/tresorerie/balance/usd"),o.send(),o.onload=function(){var e=JSON.parse(this.responseText);0<e.length&&(incomes=[],outcomes=[],budget_total=0,Array.from(e).forEach((e,t)=>{budget_total+=e.budget,incomes.push(e.income),outcomes.push(e.outcome)}),e={series:[{name:"Revenus",data:incomes},{name:"Dépenses",data:outcomes}],chart:{height:290,type:"area",toolbar:"false"},dataLabels:{enabled:!1},stroke:{curve:"smooth",width:2},xaxis:{categories:["Jan","Fév","Mar","Avr","Mai","Juin","Juil","Aou","Sep","Oct","Nov","Déc"]},yaxis:{labels:{formatter:function(e){return"usd "+e}}},colors:revenueExpensesCdfChartsColors,fill:{opacity:.06,colors:revenueExpensesCdfChartsColors,type:"solid"}},new ApexCharts(document.querySelector("#revenue-expenses-usd-charts"),e).render())}}