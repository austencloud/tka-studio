import type { CsvDataSet } from "$domain";

export interface ICsvLoader {
  loadCsvData(): Promise<CsvDataSet>;
  getCsvData(): CsvDataSet | null;
  clearCache(): void;
}
