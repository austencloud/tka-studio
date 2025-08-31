import type { CsvDataSet } from "../data-interfaces";

export interface ICsvLoader {
  loadCsvData(): Promise<CsvDataSet>;
  getCsvData(): CsvDataSet | null;
  clearCache(): void;
}
