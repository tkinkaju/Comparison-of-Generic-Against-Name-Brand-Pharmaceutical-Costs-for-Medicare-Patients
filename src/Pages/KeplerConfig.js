export const config = {
    version: "v1",
        visState: {
            filters: [],
            layers: [
                {
                    id: "n8kun5",
                    type: "geojson",
                    config: {
                        dataId: "percent_brand",
                        label: "percent_brand",
                        color: [
                            255,
                            203,
                            153
                        ],
                        highlightColor: [
                            252,
                            242,
                            26,
                            255
                        ],
                        columns: {
                            geojson: "geometry",
                        },
                        isVisible: true,
                        visConfig: {
                            "opacity": 0.8,
                            "strokeOpacity": 0.8,
                            "thickness": 0.5,
                            "strokeColor": [
                                248,
                                149,
                                112
                            ],
                            "colorRange": {
                                "name": "ColorBrewer RdBu-6",
                                "type": "diverging",
                                "category": "ColorBrewer",
                                "colors": [
                                    "#b2182b",
                                    "#ef8a62",
                                    "#fddbc7",
                                    "#d1e5f0",
                                    "#67a9cf",
                                    "#2166ac"
                                ]
                            },
                            "strokeColorRange": {
                                "name": "Global Warming",
                                "type": "sequential",
                                "category": "Uber",
                                "colors": [
                                    "#5A1846",
                                    "#900C3F",
                                    "#C70039",
                                    "#E3611C",
                                    "#F1920E",
                                    "#FFC300"
                                ]
                            },
                            "radius": 10,
                            "sizeRange": [
                                0,
                                10
                            ],
                            "radiusRange": [
                                0,
                                50
                            ],
                            "heightRange": [
                                0,
                                500
                            ],
                            "elevationScale": 5,
                            "enableElevationZoomFactor": true,
                            "stroked": true,
                            "filled": true,
                            "enable3d": false,
                            "wireframe": false
                        },
                        hidden: false,
                        textLabel: [
                            {
                                field: null,
                                color: [
                                    255,
                                    255,
                                    255
                                ],
                                size: 18,
                                offset: [
                                    0,
                                    0
                                ],
                                anchor: "start",
                                alignment: "center"
                            }
                        ]
                    },
                    visualChannels: {
                        colorField: {
                            name: "perthousand",
                            type: "real"
                        },
                        colorScale: "quantile",
                        strokeColorField: null,
                        strokeColorScale: "quantile",
                        sizeField: null,
                        sizeScale: "linear",
                        heightField: null,
                        heightScale: "linear",
                        radiusField: null,
                        radiusScale: "linear"
                    }
                }
            ],
            interactionConfig: {
                tooltip: {
                    fieldsToShow: {
                        cxds7rs86: [
                            {
                                name: "brnd_total_days",
                                format: null
                            },
                            {
                                name: "brnd_avg_cost",
                                format: null
                            },
                            {
                                name: "gen_total_day",
                                format: null
                            },
                            {
                                name: "gen_avg_cost",
                                format: null
                            },
                        ]
                    },
                    compareMode: false,
                    compareType: "absolute",
                    enabled: true
                },
                brush: {
                    size: 0.5,
                    enabled: false
                },
                geocoder: {
                    enabled: false
                },
                coordinate: {
                    enabled: false
                }
            },
            layerBlending: "normal",
            splitMaps: [],
            animationConfig: {
                currentTime: null,
                speed: 1
            }
        },
    }
