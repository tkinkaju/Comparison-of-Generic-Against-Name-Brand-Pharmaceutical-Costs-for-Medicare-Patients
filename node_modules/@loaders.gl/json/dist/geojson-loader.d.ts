import type { Loader, LoaderWithParser } from '@loaders.gl/loader-utils';
import type { JSONLoaderOptions } from './json-loader';
export type GeoJSONLoaderOptions = JSONLoaderOptions & {
    geojson?: {
        shape?: 'object-row-table';
    };
    gis?: {
        format?: 'geojson' | 'binary';
    };
};
/**
 * GeoJSON loader
 */
export declare const GeoJSONWorkerLoader: Loader;
export declare const GeoJSONLoader: LoaderWithParser;
//# sourceMappingURL=geojson-loader.d.ts.map