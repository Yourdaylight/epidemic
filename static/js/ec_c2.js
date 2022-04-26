var ec_center=echarts.init(document.getElementById("c2"),"dark")

var china_map_dataList=[{'name':'上海','value':318},{'name':'云南','value':100}]
var china_map_option = {
            tooltip: {
                    formatter:function(params,ticket, callback){
                        return params.seriesName+'<br />'+params.name+'：'+params.value
                    }
                },
            backgroundColor:"",
            visualMap: {
                min: 0,
                max: 1500,
                left: 'left',
                top: 'bottom',
                textStyle:{fontsize:8},
                inRange: {
                    color: ['#e0ffff', '#9D3030']
                },
                show:true,
                splitList:[{start:0,end:9},
                    {start:10,end:99},
                    {start:100,end:999},
                    {start:1000,end:9999},
                    {start:10000}]
            },
            geo: {
                map: 'china',
                roam: false,
                zoom:1.23,
                label: {
                    normal: {
                        show: true,
                        fontSize:'10',
                        color: 'rgba(0,0,0,0.7)'
                    }
                },
                itemStyle: {
                    normal:{
                        borderColor: 'rgba(0, 0, 0, 0.2)'
                    },
                    emphasis:{
                        areaColor: '#F3B329',
                        shadowOffsetX: 0,
                        shadowOffsetY: 0,
                        shadowBlur: 20,
                        borderWidth: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            },
            series : [
                {
                    name: '新增确诊',
                    type: 'map',
                    geoIndex: 0,
                    data:china_map_dataList
                }
            ]
        };



var world_map_dataList=[{name: 'Afghanistan', value: 28397.812},
                {name: 'Angola', value: 19549.124},
                {name: 'Albania', value: 3150.143},
                {name: 'United Arab Emirates', value: 8441.537},
            ]
var world_map_option = {
    // title: {
    //     text:"全球疫情大数据可视化",
    //     left: 'center',
    //     top: 'top'
    // },
   // tooltip: {
   //      trigger: 'item',
   //      formatter: function (params) {
   //          var value = (params.value + '').split('.');
   //          value = value[0].replace(/(\d{1,3})(?=(?:\d{3})+(?!\d))/g, '$1,')
   //                  + '.' + value[1];
   //          return params.seriesName + '<br/>' + params.name + ' : ' + value;
   //      }
   //  },
    backgroundColor:"",
    visualMap: {
        show:true,
        min: 0,
        max: 1500,
        left:'left',
        top:'bottom',
        textStyle:{fontsize:5},
        inRange: {
                    color: ['#e0ffff', '#9D3030']
                },
        splitList:[{start:10,end:999},
                    {start:1000,end:9999},
                    {start:10000,end:99999},
                    {start:100000,end:999999},
                    {start:1000000}]

    },

    series: [
        {
            name: '累计确诊',
            type: 'map',
            mapType: 'world',
            roam: true,
            itemStyle:{
                emphasis:{label:{show:true}}
            },
            data:world_map_dataList
        }
    ]
};

ec_center_option = sessionStorage.getItem("region")==="china"?china_map_option:world_map_option
ec_center.setOption(ec_center_option)