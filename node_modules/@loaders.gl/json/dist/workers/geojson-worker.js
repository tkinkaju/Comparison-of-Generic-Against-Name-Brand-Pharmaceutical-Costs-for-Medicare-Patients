"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const loader_utils_1 = require("@loaders.gl/loader-utils");
const geojson_loader_1 = require("../geojson-loader");
(0, loader_utils_1.createLoaderWorker)(geojson_loader_1.GeoJSONLoader);
