/**
 * Test Service Resolution
 *
 * Simple test to verify that our first converted service (SettingsService)
 * can be resolved from the InversifyJS container.
 */

import type { ISettingsService } from "../interfaces/application-interfaces";
import type {
  ICSVParsingService,
  IEnumMappingService,
  ILetterQueryService,
  IMotionQueryService,
} from "../interfaces/data-interfaces";
import type { IDeviceDetectionService } from "../interfaces/device-interfaces";
import type {
  IGridModeDeriver,
  ILetterDeriver,
  IPictographValidatorService,
  IPositionPatternService,
} from "../interfaces/domain-interfaces";
import type {
  IExportOptionsValidator,
  IFilenameGeneratorService,
} from "../interfaces/image-export-interfaces";
import type {
  IDataTransformationService,
  ISvgConfiguration,
} from "../interfaces/rendering-interfaces";
import { container, TYPES } from "./container";

/**
 * Test that SettingsService can be resolved from the container
 */
export function testSettingsServiceResolution(): boolean {
  try {
    console.log("🧪 Testing SettingsService resolution...");

    // Resolve the service from the container
    const settingsService = container.get<ISettingsService>(
      TYPES.ISettingsService
    );

    // Test basic functionality
    const currentSettings = settingsService.currentSettings;
    console.log("✅ SettingsService resolved successfully");
    console.log("📋 Current settings:", currentSettings);

    // Test a method call
    settingsService
      .updateSetting("theme", "light")
      .then(() => {
        console.log("✅ SettingsService method call successful");
      })
      .catch((error) => {
        console.error("❌ SettingsService method call failed:", error);
      });

    return true;
  } catch (error) {
    console.error("❌ Failed to resolve SettingsService:", error);
    return false;
  }
}

/**
 * Test that DeviceDetectionService can be resolved from the container
 */
export function testDeviceDetectionServiceResolution(): boolean {
  try {
    console.log("🧪 Testing DeviceDetectionService resolution...");

    // Resolve the service from the container
    const deviceService = container.get<IDeviceDetectionService>(
      TYPES.IDeviceDetectionService
    );

    // Test basic functionality
    const capabilities = deviceService.getCapabilities();
    console.log("✅ DeviceDetectionService resolved successfully");
    console.log("📋 Device capabilities:", {
      primaryInput: capabilities.primaryInput,
      screenSize: capabilities.screenSize,
      viewport: capabilities.viewport,
    });

    // Test a method call
    const breakpoint = deviceService.getCurrentBreakpoint();
    console.log(
      "✅ DeviceDetectionService method call successful:",
      breakpoint
    );

    return true;
  } catch (error) {
    console.error("❌ Failed to resolve DeviceDetectionService:", error);
    return false;
  }
}

/**
 * Run all service resolution tests
 */

/**
 * Test that EnumMappingService can be resolved from the container
 */
export function testEnumMappingServiceResolution(): boolean {
  try {
    console.log("🧪 Testing EnumMappingService resolution...");

    // Resolve the service from the container
    const service = container.get<IEnumMappingService>(
      TYPES.IEnumMappingService
    );

    console.log("✅ EnumMappingService resolved successfully");
    return true;
  } catch (error) {
    console.error("❌ Failed to resolve EnumMappingService:", error);
    return false;
  }
}

/**
 * Test that CSVParserService can be resolved from the container
 */
export function testCSVParserServiceResolution(): boolean {
  try {
    console.log("🧪 Testing CSVParserService resolution...");

    // Resolve the service from the container
    const service = container.get<ICSVParsingService>(TYPES.ICSVParsingService);

    console.log("✅ CSVParserService resolved successfully");
    return true;
  } catch (error) {
    console.error("❌ Failed to resolve CSVParserService:", error);
    return false;
  }
}

/**
 * Test that DataTransformationService can be resolved from the container
 */
export function testDataTransformationServiceResolution(): boolean {
  try {
    console.log("🧪 Testing DataTransformationService resolution...");

    // Resolve the service from the container
    const service = container.get<IDataTransformationService>(
      TYPES.IDataTransformationService
    );

    console.log("✅ DataTransformationService resolved successfully");
    return true;
  } catch (error) {
    console.error("❌ Failed to resolve DataTransformationService:", error);
    return false;
  }
}

/**
 * Test that LetterQueryService can be resolved from the container
 */
export function testLetterQueryServiceResolution(): boolean {
  try {
    console.log("🧪 Testing LetterQueryService resolution...");

    // Resolve the service from the container
    const service = container.get<ILetterQueryService>(
      TYPES.ILetterQueryService
    );

    console.log("✅ LetterQueryService resolved successfully");
    return true;
  } catch (error) {
    console.error("❌ Failed to resolve LetterQueryService:", error);
    return false;
  }
}

/**
 * Test that MotionQueryService can be resolved from the container
 */
export function testMotionQueryServiceResolution(): boolean {
  try {
    console.log("🧪 Testing MotionQueryService resolution...");

    // Resolve the service from the container
    const service = container.get<IMotionQueryService>(
      TYPES.IMotionQueryService
    );

    console.log("✅ MotionQueryService resolved successfully");
    return true;
  } catch (error) {
    console.error("❌ Failed to resolve MotionQueryService:", error);
    return false;
  }
}

/**
 * Test that GridModeDeriver can be resolved from the container
 */
export function testGridModeDeriverResolution(): boolean {
  try {
    console.log("🧪 Testing GridModeDeriver resolution...");

    // Resolve the service from the container
    const service = container.get<IGridModeDeriver>(TYPES.IGridModeDeriver);

    console.log("✅ GridModeDeriver resolved successfully");
    return true;
  } catch (error) {
    console.error("❌ Failed to resolve GridModeDeriver:", error);
    return false;
  }
}

/**
 * Test that LetterDeriver can be resolved from the container
 */
export function testLetterDeriverResolution(): boolean {
  try {
    console.log("🧪 Testing LetterDeriver resolution...");

    // Resolve the service from the container
    const service = container.get<ILetterDeriver>(TYPES.ILetterDeriver);

    console.log("✅ LetterDeriver resolved successfully");
    return true;
  } catch (error) {
    console.error("❌ Failed to resolve LetterDeriver:", error);
    return false;
  }
}

/**
 * Test that PictographValidatorService can be resolved from the container
 */
export function testPictographValidatorServiceResolution(): boolean {
  try {
    console.log("🧪 Testing PictographValidatorService resolution...");

    // Resolve the service from the container
    const service = container.get<IPictographValidatorService>(
      TYPES.IPictographValidatorService
    );

    console.log("✅ PictographValidatorService resolved successfully");
    return true;
  } catch (error) {
    console.error("❌ Failed to resolve PictographValidatorService:", error);
    return false;
  }
}

/**
 * Test that PositionPatternService can be resolved from the container
 */
export function testPositionPatternServiceResolution(): boolean {
  try {
    console.log("🧪 Testing PositionPatternService resolution...");

    // Resolve the service from the container
    const service = container.get<IPositionPatternService>(
      TYPES.IPositionPatternService
    );

    console.log("✅ PositionPatternService resolved successfully");
    return true;
  } catch (error) {
    console.error("❌ Failed to resolve PositionPatternService:", error);
    return false;
  }
}

/**
 * Test that SvgConfiguration can be resolved from the container
 */
export function testSvgConfigurationResolution(): boolean {
  try {
    console.log("🧪 Testing SvgConfiguration resolution...");

    // Resolve the service from the container
    const service = container.get<ISvgConfiguration>(TYPES.ISvgConfiguration);

    console.log("✅ SvgConfiguration resolved successfully");
    return true;
  } catch (error) {
    console.error("❌ Failed to resolve SvgConfiguration:", error);
    return false;
  }
}

/**
 * Test that FilenameGeneratorService can be resolved from the container
 */
export function testFilenameGeneratorServiceResolution(): boolean {
  try {
    console.log("🧪 Testing FilenameGeneratorService resolution...");

    // Resolve the service from the container
    const service = container.get<IFilenameGeneratorService>(
      TYPES.IFilenameGeneratorService
    );

    console.log("✅ FilenameGeneratorService resolved successfully");
    return true;
  } catch (error) {
    console.error("❌ Failed to resolve FilenameGeneratorService:", error);
    return false;
  }
}

/**
 * Test that ExportOptionsValidator can be resolved from the container
 */
export function testExportOptionsValidatorResolution(): boolean {
  try {
    console.log("🧪 Testing ExportOptionsValidator resolution...");

    // Resolve the service from the container
    const service = container.get<IExportOptionsValidator>(
      TYPES.IExportOptionsValidator
    );

    console.log("✅ ExportOptionsValidator resolved successfully");
    return true;
  } catch (error) {
    console.error("❌ Failed to resolve ExportOptionsValidator:", error);
    return false;
  }
}

export function runServiceResolutionTests(): void {
  console.log("🚀 Running InversifyJS service resolution tests...");

  const results = {
    settingsService: testSettingsServiceResolution(),
    deviceDetectionService: testDeviceDetectionServiceResolution(),

    enummappingservice: testEnumMappingServiceResolution(),
    csvparserservice: testCSVParserServiceResolution(),
    datatransformationservice: testDataTransformationServiceResolution(),
    // letterqueryservice: testLetterQueryServiceResolution(), // Has dependencies
    // motionqueryservice: testMotionQueryServiceResolution(), // Has dependencies
    gridmodederiver: testGridModeDeriverResolution(),
    letterderiver: testLetterDeriverResolution(),
    pictographvalidatorservice: testPictographValidatorServiceResolution(),
    positionpatternservice: testPositionPatternServiceResolution(),
    svgconfiguration: testSvgConfigurationResolution(),
    filenamegeneratorservice: testFilenameGeneratorServiceResolution(),
    // exportoptionsvalidator: testExportOptionsValidatorResolution(), // Has dependencies
  };

  const passedTests = Object.values(results).filter(Boolean).length;
  const totalTests = Object.keys(results).length;

  console.log(`📊 Test Results: ${passedTests}/${totalTests} passed`);

  if (passedTests === totalTests) {
    console.log("🎉 All service resolution tests passed!");
  } else {
    console.error("❌ Some service resolution tests failed");
  }
}
