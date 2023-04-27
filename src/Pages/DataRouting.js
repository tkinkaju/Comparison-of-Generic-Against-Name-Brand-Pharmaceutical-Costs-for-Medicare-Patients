import { processCsvData } from '@kepler.gl/processors'
import woob from './../../map source data/2020/statesSummaries/Sertraline Hcl'

export default async function(year, drug, scale){
    const modulePathName = (year+'/'+scale+'/'+drug);
    const dataFile = await import('./../../map source data/'+modulePathName)
    console.log(modulePathName)
    console.log(dataFile["default"])
    return processCsvData(dataFile["default"])
}