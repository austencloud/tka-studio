import type { ContainerModuleLoadOptions } from "inversify";
import { ContainerModule } from "inversify";
import { OptionFilterer } from "../../../modules/build/construct/option-picker/services/implementations/OptionFilterer";
import { BackgroundService } from "../../background";
import {
  CsvLoader,
  CSVParser,
  EnumMapper,
} from "../../foundation";
import { DataTransformer } from "../../pictograph/shared/services/implementations/DataTransformer";
import { TYPES } from "../types";

export const dataModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === DATA SERVICES ===
    options.bind(TYPES.ICSVLoader).to(CsvLoader);
    options.bind(TYPES.ICSVParser).to(CSVParser);
    options.bind(TYPES.IDataTransformer).to(DataTransformer);
    options.bind(TYPES.IEnumMapper).to(EnumMapper);
    options.bind(TYPES.IOptionFilterer).to(OptionFilterer);

    // === BACKGROUND SERVICES ===
    options.bind(TYPES.IBackgroundService).to(BackgroundService);
  }
);
