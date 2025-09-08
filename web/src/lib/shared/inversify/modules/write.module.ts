import type { ContainerModuleLoadOptions } from "inversify";
import { ContainerModule } from "inversify";
import { ActService } from "../../../modules/write/services/implementations/ActService";
import { MusicPlayerService } from "../../../modules/write/services/implementations/MusicPlayerService";
import { TYPES } from "../types";

export const writeModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === WRITE TAB SERVICES ===
    options.bind(TYPES.IActService).to(ActService);
    options.bind(TYPES.IMusicPlayerService).to(MusicPlayerService);
  }
);
