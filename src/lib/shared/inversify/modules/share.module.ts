/**
 * Share Module - InversifyJS Container Module
 *
 * Binds share services for dependency injection.
 */

import type { ContainerModuleLoadOptions } from "inversify";
import { ContainerModule } from "inversify";
import {
  ShareService,
  InstagramLinkService,
  InstagramAuthService,
  InstagramGraphApiService,
  MediaBundlerService,
} from "../../../modules/create/share/services/implementations";
import { TYPES } from "../types";

export const shareModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === SHARE SERVICES ===
    options.bind(TYPES.IShareService).to(ShareService);
    options.bind(TYPES.IInstagramLinkService).to(InstagramLinkService);
    options.bind(TYPES.IInstagramAuthService).to(InstagramAuthService);
    options.bind(TYPES.IInstagramGraphApiService).to(InstagramGraphApiService);
    options.bind(TYPES.IMediaBundlerService).to(MediaBundlerService);
  }
);
