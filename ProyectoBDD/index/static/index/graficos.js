const getOptionChart=async()=>{
    try{
        const response=await fetch("http://127.0.0.1:8000/get-chart/");
        return await response.json();
    }catch (ex) {
        alert(ex);
    }
};

const initChart = async()=>{
    // const myChart=echarts.init(document.getElementById("chart"));

    // myChart.setOption(await getOptionChart());
    // myChart.resize();

    const chartData = await getOptionChart();

    const chart1Element = document.getElementById("chart1");
    const chart2Element = document.getElementById("chart2");
    const chart3Element = document.getElementById("chart3");

    if (chart1Element) {
        const chart1 = echarts.init(chart1Element);
        chart1.setOption(chartData.chart1);
        chart1.resize();
    }

    if (chart2Element) {
        const chart2 = echarts.init(chart2Element);
        chart2.setOption(chartData.chart2);
        chart2.resize();
    }

    if (chart3Element) {
        const chart3 = echarts.init(chart3Element);
        chart3.setOption(chartData.chart3);
        chart3.resize();
    }
};

window.addEventListener("load", async()=>{
    await initChart();
});

