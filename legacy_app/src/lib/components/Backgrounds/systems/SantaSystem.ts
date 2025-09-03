// src/lib/components/Backgrounds/systems/SantaSystem.ts
import type { Dimensions, SantaState } from '../types/types';
import { SantaConfig, SeasonalConfig } from '../config';

export const createSantaSystem = () => {
  const config = SantaConfig;
  let santaImageLeft: HTMLImageElement | null = null;
  let santaImageRight: HTMLImageElement | null = null;
  let imageLoaded = false;

  const preloadImages = (): Promise<void> => {
    return new Promise((resolve) => {
      if (typeof window === 'undefined') {
        resolve();
        return;
      }

      santaImageLeft = new Image();
      santaImageRight = new Image();

      let loadedCount = 0;

      const onLoad = () => {
        loadedCount++;
        if (loadedCount === 2) {
          imageLoaded = true;
          resolve();
        }
      };

      santaImageLeft.onload = onLoad;
      santaImageRight.onload = onLoad;

      santaImageLeft.src = config.assets.leftImage;
      santaImageRight.src = config.assets.rightImage;
    });
  };

  const getRandomInterval = (): number => {
    return (
      Math.floor(Math.random() * (config.maxInterval - config.minInterval + 1)) + config.minInterval
    );
  };

  const getRandomSpeed = (): number => {
    return Math.random() * (config.maxSpeed - config.minSpeed) + config.minSpeed;
  };

  const calculateSize = (width: number): number => {
    const sizeByPercent = width * config.maxSizePercent;
    return Math.min(sizeByPercent, config.maxSizePx);
  };

  const initialState: SantaState = {
    x: -100,
    y: 0,
    speed: 0,
    active: false,
    direction: 1,
    opacity: config.opacity
  };

  const update = (
    state: SantaState,
    { width, height }: Dimensions,
    isDecember: boolean
  ): SantaState => {
    const isSeasonalEnabled =
      SeasonalConfig.enabled && (isDecember || SeasonalConfig.isChristmas());

    if (!state.active && isSeasonalEnabled) {
      if (Math.random() < 0.01) {
        const direction = Math.random() > 0.5 ? 1 : -1;
        const startX = direction > 0 ? -calculateSize(width) : width + calculateSize(width);
        const randomY =
          height *
          (Math.random() * (config.maxY - config.minY) +
            config.minY);

        return {
          x: startX,
          y: randomY,
          speed: getRandomSpeed(),
          active: true,
          direction: direction,
          opacity: config.opacity
        };
      }
      return state;
    } else if (state.active) {
      const newX = state.x + state.speed * width * state.direction;

      if (
        (state.direction > 0 && newX > width + calculateSize(width)) ||
        (state.direction < 0 && newX < -calculateSize(width))
      ) {
        return {
          ...initialState
        };
      }

      return {
        ...state,
        x: newX
      };
    }

    return state;
  };

  const draw = (state: SantaState, ctx: CanvasRenderingContext2D, { width }: Dimensions): void => {
    if (!state.active || !ctx || !imageLoaded) return;

    const santaSize = calculateSize(width);
    const santaImage = state.direction > 0 ? santaImageRight : santaImageLeft;

    if (!santaImage) return;

    ctx.save();
    ctx.globalAlpha = state.opacity;

    ctx.drawImage(
      santaImage,
      state.x - santaSize / 2,
      state.y - santaSize / 2,
      santaSize,
      santaSize
    );

    ctx.restore();
  };

  return {
    preloadImages,
    initialState,
    update,
    draw
  };
};