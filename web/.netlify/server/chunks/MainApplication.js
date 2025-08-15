import { T as derived, e as escape_html, i as attr_style, f as stringify, g as getContext, h as head, p as pop, a as push } from "./index2.js";
import { P as PngMetadataExtractor } from "./png-metadata-extractor.js";
import "clsx";
/* empty css                                       */
var MotionType = /* @__PURE__ */ ((MotionType2) => {
  MotionType2["PRO"] = "pro";
  MotionType2["ANTI"] = "anti";
  MotionType2["FLOAT"] = "float";
  MotionType2["DASH"] = "dash";
  MotionType2["STATIC"] = "static";
  return MotionType2;
})(MotionType || {});
var RotationDirection = /* @__PURE__ */ ((RotationDirection2) => {
  RotationDirection2["CLOCKWISE"] = "cw";
  RotationDirection2["COUNTER_CLOCKWISE"] = "ccw";
  RotationDirection2["NO_ROTATION"] = "no_rot";
  return RotationDirection2;
})(RotationDirection || {});
var Orientation = /* @__PURE__ */ ((Orientation2) => {
  Orientation2["IN"] = "in";
  Orientation2["OUT"] = "out";
  Orientation2["CLOCK"] = "clock";
  Orientation2["COUNTER"] = "counter";
  return Orientation2;
})(Orientation || {});
var Location = /* @__PURE__ */ ((Location2) => {
  Location2["NORTH"] = "n";
  Location2["EAST"] = "e";
  Location2["SOUTH"] = "s";
  Location2["WEST"] = "w";
  Location2["NORTHEAST"] = "ne";
  Location2["SOUTHEAST"] = "se";
  Location2["SOUTHWEST"] = "sw";
  Location2["NORTHWEST"] = "nw";
  return Location2;
})(Location || {});
var GridMode = /* @__PURE__ */ ((GridMode2) => {
  GridMode2["DIAMOND"] = "diamond";
  GridMode2["BOX"] = "box";
  return GridMode2;
})(GridMode || {});
var ArrowType = /* @__PURE__ */ ((ArrowType2) => {
  ArrowType2["BLUE"] = "blue";
  ArrowType2["RED"] = "red";
  return ArrowType2;
})(ArrowType || {});
var PropType = /* @__PURE__ */ ((PropType2) => {
  PropType2["STAFF"] = "staff";
  PropType2["CLUB"] = "club";
  PropType2["HOOP"] = "hoop";
  PropType2["BUUGENG"] = "buugeng";
  PropType2["FAN"] = "fan";
  PropType2["TRIAD"] = "triad";
  PropType2["FRACTALS"] = "fractals";
  PropType2["MINIHOOP"] = "minihoop";
  PropType2["BIGBALL"] = "bigball";
  PropType2["CRYSTAL"] = "crystal";
  return PropType2;
})(PropType || {});
const initState = {
  initializationProgress: 0
};
function getInitializationProgress() {
  return initState.initializationProgress;
}
({
  gridMode: GridMode.DIAMOND
});
function createServiceInterface$1(token, implementation) {
  return { token, implementation };
}
class ApplicationInitializationService {
  constructor(settingsService, persistenceService) {
    this.settingsService = settingsService;
    this.persistenceService = persistenceService;
  }
  /**
   * Initialize the application
   */
  async initialize() {
    try {
      console.log("🚀 Starting TKA V2 Modern initialization...");
      await this.initializeSettings();
      await this.initializePersistence();
      await this.performStartupChecks();
      await this.loadInitialData();
      console.log("✅ TKA V2 Modern initialization complete");
    } catch (error) {
      console.error("❌ Application initialization failed:", error);
      throw new Error(
        `Initialization failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Initialize settings
   */
  async initializeSettings() {
    try {
      console.log("⚙️ Loading application settings...");
      await this.settingsService.loadSettings();
      console.log("✅ Settings loaded successfully");
    } catch (error) {
      console.warn("⚠️ Failed to load settings, using defaults:", error);
    }
  }
  /**
   * Initialize persistence layer
   */
  async initializePersistence() {
    try {
      console.log("💾 Initializing persistence layer...");
      if (typeof Storage === "undefined") {
        throw new Error("LocalStorage is not available");
      }
      const testKey = "tka-v2-test";
      localStorage.setItem(testKey, "test");
      localStorage.removeItem(testKey);
      console.log("✅ Persistence layer initialized");
    } catch (error) {
      console.error("❌ Persistence initialization failed:", error);
      throw new Error(
        `Persistence initialization failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Perform startup checks
   */
  async performStartupChecks() {
    console.log("🔍 Performing startup checks...");
    const checks = [
      this.checkSVGSupport(),
      this.checkES6Support(),
      this.checkLocalStorageSpace()
    ];
    const results = await Promise.allSettled(checks);
    const failures = results.filter((result) => result.status === "rejected");
    if (failures.length > 0) {
      console.warn("⚠️ Some startup checks failed:", failures);
    }
    console.log("✅ Startup checks complete");
  }
  /**
   * Load initial data
   */
  async loadInitialData() {
    try {
      console.log("📂 Loading initial data...");
      const sequences = await this.persistenceService.loadAllSequences();
      console.log(`📊 Found ${sequences.length} existing sequences`);
      console.log("✅ Initial data loaded");
    } catch (error) {
      console.warn("⚠️ Failed to load initial data:", error);
    }
  }
  /**
   * Check SVG support
   */
  async checkSVGSupport() {
    if (!document.createElementNS) {
      throw new Error("SVG support not available");
    }
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    if (!svg || typeof svg.createSVGRect !== "function") {
      throw new Error("SVG functionality not fully supported");
    }
  }
  /**
   * Check ES6 support
   */
  async checkES6Support() {
    if (typeof Promise === "undefined") {
      throw new Error("Promise support required");
    }
    if (typeof Map === "undefined") {
      throw new Error("Map support required");
    }
    if (typeof Set === "undefined") {
      throw new Error("Set support required");
    }
  }
  /**
   * Check localStorage space
   */
  async checkLocalStorageSpace() {
    try {
      const testData = "x".repeat(1024 * 1024);
      const testKey = "tka-v2-space-test";
      localStorage.setItem(testKey, testData);
      localStorage.removeItem(testKey);
    } catch {
      throw new Error("Insufficient localStorage space");
    }
  }
  /**
   * Get initialization status
   */
  getInitializationStatus() {
    return {
      isInitialized: true,
      version: "2.0.0",
      timestamp: (/* @__PURE__ */ new Date()).toISOString()
    };
  }
}
function createSequenceData(data = {}) {
  const result = {
    id: data.id ?? crypto.randomUUID(),
    name: data.name ?? "",
    word: data.word ?? "",
    beats: data.beats ?? [],
    thumbnails: data.thumbnails ?? [],
    is_favorite: data.is_favorite ?? false,
    is_circular: data.is_circular ?? false,
    tags: data.tags ?? [],
    metadata: data.metadata ?? {},
    // Optional properties - only include if defined
    ...data.sequence_length !== void 0 && {
      sequence_length: data.sequence_length
    },
    ...data.author !== void 0 && { author: data.author },
    ...data.level !== void 0 && { level: data.level },
    ...data.date_added !== void 0 && { date_added: data.date_added },
    ...data.grid_mode !== void 0 && { grid_mode: data.grid_mode },
    ...data.prop_type !== void 0 && { prop_type: data.prop_type },
    ...data.starting_position !== void 0 && {
      starting_position: data.starting_position
    },
    ...data.difficulty_level !== void 0 && {
      difficulty_level: data.difficulty_level
    },
    ...data.start_position !== void 0 && {
      start_position: data.start_position
    }
  };
  return result;
}
function updateSequenceData(sequence, updates) {
  return {
    ...sequence,
    ...updates
  };
}
class SequenceStateService {
  // Core sequence state
  #currentSequence = null;
  #selectedBeatIndex = -1;
  #isLoading = false;
  #error = null;
  #_currentSequence = derived(() => this.#currentSequence);
  get currentSequence() {
    return this.#_currentSequence();
  }
  set currentSequence($$value) {
    return this.#_currentSequence($$value);
  }
  #_selectedBeatIndex = derived(() => this.#selectedBeatIndex);
  get selectedBeatIndex() {
    return this.#_selectedBeatIndex();
  }
  set selectedBeatIndex($$value) {
    return this.#_selectedBeatIndex($$value);
  }
  #selectedBeat = derived(() => () => {
    if (this.#currentSequence && this.#selectedBeatIndex >= 0) {
      return this.#currentSequence.beats[this.#selectedBeatIndex] ?? null;
    }
    return null;
  });
  get selectedBeat() {
    return this.#selectedBeat();
  }
  set selectedBeat($$value) {
    return this.#selectedBeat($$value);
  }
  #_isLoading = derived(() => this.#isLoading);
  get isLoading() {
    return this.#_isLoading();
  }
  set isLoading($$value) {
    return this.#_isLoading($$value);
  }
  #_error = derived(() => this.#error);
  get error() {
    return this.#_error();
  }
  set error($$value) {
    return this.#_error($$value);
  }
  #hasSequence = derived(() => () => this.#currentSequence !== null);
  get hasSequence() {
    return this.#hasSequence();
  }
  set hasSequence($$value) {
    return this.#hasSequence($$value);
  }
  #beatCount = derived(() => () => this.#currentSequence?.beats.length ?? 0);
  get beatCount() {
    return this.#beatCount();
  }
  set beatCount($$value) {
    return this.#beatCount($$value);
  }
  setCurrentSequence(sequence) {
    this.#currentSequence = sequence;
    this.#selectedBeatIndex = -1;
    this.#error = null;
  }
  selectBeat(index) {
    if (this.#currentSequence && index >= 0 && index < this.#currentSequence.beats.length) {
      this.#selectedBeatIndex = index;
    } else {
      this.#selectedBeatIndex = -1;
    }
  }
  updateBeat(index, beatData) {
    if (!this.#currentSequence || index < 0 || index >= this.#currentSequence.beats.length) {
      return;
    }
    const newBeats = [...this.#currentSequence.beats];
    newBeats[index] = beatData;
    this.#currentSequence = updateSequenceData(this.#currentSequence, { beats: newBeats });
  }
  addBeat(beatData) {
    if (!this.#currentSequence) return;
    const newBeats = [...this.#currentSequence.beats, beatData];
    this.#currentSequence = updateSequenceData(this.#currentSequence, { beats: newBeats });
  }
  removeBeat(index) {
    if (!this.#currentSequence || index < 0 || index >= this.#currentSequence.beats.length) {
      return;
    }
    const newBeats = this.#currentSequence.beats.filter((_, i) => i !== index);
    this.#currentSequence = updateSequenceData(this.#currentSequence, { beats: newBeats });
    if (this.#selectedBeatIndex >= newBeats.length) {
      this.#selectedBeatIndex = newBeats.length - 1;
    }
  }
  setLoading(loading) {
    this.#isLoading = loading;
  }
  setError(error) {
    this.#error = error;
  }
  clearError() {
    this.#error = null;
  }
  setStartPosition(startPosition) {
    if (!this.#currentSequence) return;
    this.#currentSequence = updateSequenceData(this.#currentSequence, { start_position: startPosition });
  }
  createNewSequence(name, length = 16) {
    const sequence = createSequenceData({
      name,
      beats: Array.from({ length }, (_, i) => ({
        id: crypto.randomUUID(),
        beat_number: i + 1,
        duration: 1,
        blue_reversal: false,
        red_reversal: false,
        is_blank: true,
        metadata: {}
      }))
    });
    this.setCurrentSequence(sequence);
  }
}
const sequenceStateService = new SequenceStateService();
class ConstructTabCoordinationService {
  constructor(sequenceService, startPositionService) {
    this.sequenceService = sequenceService;
    this.startPositionService = startPositionService;
    console.log("🎭 ConstructTabCoordinationService initialized");
  }
  components = {};
  isHandlingSequenceModification = false;
  setupComponentCoordination(components) {
    console.log(
      "🎭 Setting up component coordination:",
      Object.keys(components)
    );
    this.components = components;
    this.connectComponentSignals();
  }
  async handleSequenceModified(sequence) {
    if (this.isHandlingSequenceModification) {
      return;
    }
    console.log("🎭 Handling sequence modification:", sequence.id);
    try {
      this.isHandlingSequenceModification = true;
      sequenceStateService.setCurrentSequence(sequence);
      await this.updateUIBasedOnSequence(sequence);
      this.notifyComponents("sequence_modified", { sequence });
    } catch (error) {
      console.error("❌ Error handling sequence modification:", error);
    } finally {
      this.isHandlingSequenceModification = false;
    }
  }
  async handleStartPositionSet(startPosition) {
    console.log(
      "🎭 Handling start position set:",
      startPosition.pictograph_data?.id
    );
    try {
      sequenceStateService.setLoading(true);
      sequenceStateService.clearError();
      await this.startPositionService.setStartPosition(startPosition);
      console.log(
        "🎭 Creating sequence with start position stored separately from beats"
      );
      const newSequence = await this.sequenceService.createSequence({
        name: `Sequence ${(/* @__PURE__ */ new Date()).toLocaleTimeString()}`,
        length: 0,
        // Start with 0 beats - beats will be added progressively
        gridMode: GridMode.DIAMOND,
        // Default grid mode
        propType: "staff"
        // Default prop type
      });
      console.log("🎭 Setting start position in sequence.start_position field");
      await this.sequenceService.setSequenceStartPosition(
        newSequence.id,
        startPosition
      );
      const updatedSequence = await this.sequenceService.getSequence(
        newSequence.id
      );
      if (updatedSequence) {
        console.log("🔄 Updating singleton sequence state with new sequence");
        sequenceStateService.setCurrentSequence(updatedSequence);
        sequenceStateService.setLoading(false);
        this.notifyComponents("sequenceCreated", {
          sequence: updatedSequence,
          startPosition
        });
        console.log(
          "🎯 Set updated sequence as current sequence:",
          updatedSequence.id,
          "beats:",
          updatedSequence.beats.length,
          "start_position:",
          updatedSequence.start_position?.pictograph_data?.id
        );
        console.log(
          "✅ Updated sequence state - UI should now transition to option picker"
        );
      } else {
        console.error("❌ Failed to reload updated sequence");
        sequenceStateService.setLoading(false);
        sequenceStateService.setError("Failed to create sequence with start position");
        return;
      }
      console.log("✅ Sequence created with start position stored separately");
      this.notifyComponents("start_position_set", { startPosition });
      this.notifyComponents("ui_state_update_requested", {
        action: "hide_start_position_picker"
      });
      console.log("🎭 UI state should now automatically show option picker");
      await this.handleUITransitionRequest("option_picker");
    } catch (error) {
      console.error("❌ Error handling start position set:", error);
      sequenceStateService.setLoading(false);
      sequenceStateService.setError(
        `Failed to set start position: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  async handleBeatAdded(beatData) {
    console.log("🎭 Handling beat added:", beatData.beat_number);
    try {
      const currentSequence = sequenceStateService.currentSequence;
      if (!currentSequence) {
        console.error("❌ No current sequence available for adding beat");
        return;
      }
      console.log(`🎭 Adding beat to sequence: ${currentSequence.id}`);
      if ("addBeat" in this.sequenceService && typeof this.sequenceService.addBeat === "function") {
        await this.sequenceService.addBeat(currentSequence.id, beatData);
        const updatedSequence = await this.sequenceService.getSequence(currentSequence.id);
        if (updatedSequence) {
          sequenceStateService.setCurrentSequence(updatedSequence);
          console.log("✅ Beat added and sequence state updated");
        }
      } else {
        sequenceStateService.addBeat(beatData);
        console.log("✅ Beat added directly to state");
      }
      this.notifyComponents("beat_added", { beatData });
    } catch (error) {
      console.error("❌ Error handling beat added:", error);
      sequenceStateService.setError(
        `Failed to add beat: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  async handleGenerationRequest(config) {
    console.log("🎭 Handling generation request:", config);
    try {
      this.notifyComponents("generation_requested", { config });
      setTimeout(() => {
        this.notifyComponents("generation_completed", {
          success: true,
          message: "Generation completed"
        });
      }, 1e3);
    } catch (error) {
      console.error("❌ Error handling generation request:", error);
    }
  }
  async handleUITransitionRequest(targetPanel) {
    console.log("🎭 Handling UI transition request to:", targetPanel);
    try {
      const transitionEvent = new CustomEvent("construct-tab-transition", {
        detail: { targetPanel },
        bubbles: true
      });
      if (typeof window !== "undefined") {
        document.dispatchEvent(transitionEvent);
      }
      this.notifyComponents("ui_transition", { targetPanel });
    } catch (error) {
      console.error("❌ Error handling UI transition:", error);
    }
  }
  connectComponentSignals() {
    if (typeof window !== "undefined") {
      document.addEventListener("start-position-selected", (event) => {
        this.handleStartPositionSet(event.detail.startPosition);
      });
      document.addEventListener("option-selected", (event) => {
        this.handleBeatAdded(event.detail.beatData);
      });
      document.addEventListener("sequence-modified", (event) => {
        this.handleSequenceModified(event.detail.sequence);
      });
    }
  }
  async updateUIBasedOnSequence(sequence) {
    console.log("🎭 Updating UI based on sequence state");
    try {
      const hasStartPosition = sequence?.start_position != null;
      const hasBeats = sequence && sequence.beats && sequence.beats.length > 0;
      let targetPanel;
      if (hasStartPosition || hasBeats) {
        targetPanel = "option_picker";
        console.log("🎯 UI should show option picker (has start position or beats)");
      } else {
        targetPanel = "start_position_picker";
        console.log("🎯 UI should show start position picker (no start position or beats)");
      }
      await this.handleUITransitionRequest(targetPanel);
    } catch (error) {
      console.error("❌ Error updating UI based on sequence:", error);
    }
  }
  hasStartPosition(sequence) {
    return sequence?.start_position != null;
  }
  notifyComponents(eventType, data) {
    console.log(`🎭 Notifying components of ${eventType}:`, data);
    Object.entries(this.components).forEach(([name, component]) => {
      if (component && typeof component.handleEvent === "function") {
        try {
          component.handleEvent(eventType, data);
        } catch (error) {
          console.error(`❌ Error notifying component ${name}:`, error);
        }
      }
    });
    if (typeof window !== "undefined") {
      const event = new CustomEvent(`construct-coordination-${eventType}`, {
        detail: data,
        bubbles: true
      });
      document.dispatchEvent(event);
    }
  }
}
class DeviceDetectionService {
  capabilities = null;
  listeners = [];
  resizeObserver = null;
  constructor() {
    this.detectCapabilities();
    this.setupListeners();
  }
  getCapabilities() {
    if (!this.capabilities) {
      this.detectCapabilities();
    }
    if (!this.capabilities) {
      throw new Error("Failed to detect device capabilities");
    }
    return this.capabilities;
  }
  getResponsiveSettings() {
    const caps = this.getCapabilities();
    const minTouchTarget = caps.primaryInput === "touch" ? 48 : 32;
    const elementSpacing = caps.primaryInput === "touch" ? 16 : 8;
    const allowScrolling = caps.screenSize === "mobile" || caps.screenSize === "tablet";
    let layoutDensity = "comfortable";
    if (caps.screenSize === "mobile") {
      layoutDensity = "comfortable";
    } else if (caps.screenSize === "desktop" && caps.primaryInput === "mouse") {
      layoutDensity = "compact";
    } else {
      layoutDensity = "spacious";
    }
    const fontScaling = caps.screenSize === "mobile" ? 1.1 : 1;
    return {
      minTouchTarget,
      elementSpacing,
      allowScrolling,
      layoutDensity,
      fontScaling
    };
  }
  isTouchPrimary() {
    return this.getCapabilities().primaryInput === "touch";
  }
  shouldOptimizeForTouch() {
    const caps = this.getCapabilities();
    return caps.primaryInput === "touch" || caps.primaryInput === "hybrid";
  }
  getCurrentBreakpoint() {
    const { width } = this.getCapabilities().viewport;
    if (width < 768) return "mobile";
    if (width < 1024) return "tablet";
    if (width < 1440) return "desktop";
    return "large-desktop";
  }
  onCapabilitiesChanged(callback) {
    this.listeners.push(callback);
    return () => {
      const index = this.listeners.indexOf(callback);
      if (index > -1) {
        this.listeners.splice(index, 1);
      }
    };
  }
  detectCapabilities() {
    const viewport = {
      width: window.innerWidth,
      height: window.innerHeight
    };
    const hasTouch = this.detectTouch();
    const hasPrecisePointer = this.detectPrecisePointer();
    const hasKeyboard = this.detectKeyboard();
    const screenSize = this.determineScreenSize(viewport.width);
    const primaryInput = this.determinePrimaryInput(
      hasTouch,
      hasPrecisePointer,
      screenSize
    );
    this.capabilities = {
      primaryInput,
      screenSize,
      hasTouch,
      hasPrecisePointer,
      hasKeyboard,
      viewport,
      pixelRatio: window.devicePixelRatio || 1,
      colorDepth: screen.colorDepth || 24,
      supportsHDR: this.detectHDRSupport(),
      hardwareConcurrency: navigator.hardwareConcurrency || 4,
      memoryEstimate: this.estimateMemory(),
      connectionSpeed: this.detectConnectionSpeed()
    };
    this.updateCSSProperties();
  }
  detectTouch() {
    return "ontouchstart" in window || navigator.maxTouchPoints > 0 || // Legacy IE support
    (navigator.msMaxTouchPoints ?? 0) > 0;
  }
  detectPrecisePointer() {
    return window.matchMedia("(pointer: fine)").matches;
  }
  detectKeyboard() {
    return window.matchMedia("(pointer: fine)").matches;
  }
  determineScreenSize(width) {
    if (width < 768) return "mobile";
    if (width < 1024) return "tablet";
    return "desktop";
  }
  determinePrimaryInput(hasTouch, hasPrecisePointer, screenSize) {
    if (screenSize === "mobile") return "touch";
    if (screenSize === "desktop" && !hasTouch) return "mouse";
    if (screenSize === "desktop" && hasTouch && hasPrecisePointer)
      return "hybrid";
    if (screenSize === "tablet") {
      return hasPrecisePointer ? "hybrid" : "touch";
    }
    return hasTouch ? "touch" : "mouse";
  }
  updateCSSProperties() {
    if (!this.capabilities) return;
    const settings = this.getResponsiveSettings();
    document.documentElement.style.setProperty(
      "--min-touch-target",
      `${settings.minTouchTarget}px`
    );
    document.documentElement.style.setProperty(
      "--element-spacing",
      `${settings.elementSpacing}px`
    );
    document.documentElement.style.setProperty(
      "--font-scaling",
      settings.fontScaling.toString()
    );
    document.documentElement.setAttribute(
      "data-device-type",
      this.capabilities.primaryInput
    );
    document.documentElement.setAttribute(
      "data-screen-size",
      this.capabilities.screenSize
    );
    document.documentElement.setAttribute(
      "data-layout-density",
      settings.layoutDensity
    );
  }
  setupListeners() {
    const handleResize = () => {
      const oldCapabilities = this.capabilities;
      this.detectCapabilities();
      if (this.hasCapabilitiesChanged(oldCapabilities, this.capabilities)) {
        this.notifyListeners();
      }
    };
    const handleOrientationChange = () => {
      setTimeout(handleResize, 100);
    };
    window.addEventListener("resize", handleResize);
    window.addEventListener("orientationchange", handleOrientationChange);
    if ("ResizeObserver" in window) {
      this.resizeObserver = new ResizeObserver(handleResize);
      this.resizeObserver.observe(document.documentElement);
    }
    let hasDetectedMouse = false;
    const handleMouseMove = () => {
      if (!hasDetectedMouse) {
        hasDetectedMouse = true;
        const oldCapabilities = this.capabilities;
        this.detectCapabilities();
        if (this.hasCapabilitiesChanged(oldCapabilities, this.capabilities)) {
          this.notifyListeners();
        }
      }
    };
    window.addEventListener("mousemove", handleMouseMove, { once: true });
  }
  hasCapabilitiesChanged(old, current) {
    if (!old || !current) return true;
    return old.primaryInput !== current.primaryInput || old.screenSize !== current.screenSize || old.viewport.width !== current.viewport.width || old.viewport.height !== current.viewport.height;
  }
  notifyListeners() {
    if (this.capabilities) {
      const capabilities = this.capabilities;
      this.listeners.forEach((callback) => callback(capabilities));
    }
  }
  // Cleanup method for proper disposal
  dispose() {
    this.listeners = [];
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
      this.resizeObserver = null;
    }
  }
  detectHDRSupport() {
    if (typeof window !== "undefined" && window.matchMedia) {
      return window.matchMedia("(dynamic-range: high)").matches || window.matchMedia("(color-gamut: p3)").matches;
    }
    return false;
  }
  estimateMemory() {
    if ("deviceMemory" in navigator) {
      return navigator.deviceMemory * 1024;
    }
    const hardwareConcurrency = navigator.hardwareConcurrency || 4;
    if (hardwareConcurrency >= 8) return 8192;
    if (hardwareConcurrency >= 4) return 4096;
    return 2048;
  }
  detectConnectionSpeed() {
    if ("connection" in navigator) {
      const connection = navigator.connection;
      if (connection.effectiveType) {
        switch (connection.effectiveType) {
          case "slow-2g":
          case "2g":
            return "slow";
          case "3g":
            return "medium";
          case "4g":
          default:
            return "fast";
        }
      }
    }
    return void 0;
  }
}
class ExportService {
  // pictographService reserved for future richer rendering; omitted to reduce lint noise
  constructor(_pictographService) {
  }
  /**
   * Export sequence as PNG image
   */
  async exportSequenceAsImage(sequence, options) {
    try {
      console.log(`Exporting sequence "${sequence.name}" as image`);
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      if (!ctx) {
        throw new Error("Canvas 2D context not available");
      }
      const beatSize = options.beatSize;
      const spacing = options.spacing;
      const totalBeats = sequence.beats.length;
      const cols = Math.ceil(Math.sqrt(totalBeats));
      const rows = Math.ceil(totalBeats / cols);
      canvas.width = cols * beatSize + (cols - 1) * spacing;
      canvas.height = rows * beatSize + (rows - 1) * spacing;
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      for (let i = 0; i < totalBeats; i++) {
        const beat = sequence.beats[i];
        const col = i % cols;
        const row = Math.floor(i / cols);
        const x = col * (beatSize + spacing);
        const y = row * (beatSize + spacing);
        await this.renderBeatPlaceholder(ctx, beat, x, y, beatSize);
      }
      if (options.includeTitle) {
        this.renderTitle(ctx, sequence.name, canvas.width);
      }
      return new Promise((resolve2, reject) => {
        canvas.toBlob((blob) => {
          if (blob) {
            resolve2(blob);
          } else {
            reject(new Error("Failed to create image blob"));
          }
        }, "image/png");
      });
    } catch (error) {
      console.error("Failed to export sequence as image:", error);
      throw new Error(
        `Export failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Export sequence as JSON
   */
  async exportSequenceAsJson(sequence) {
    try {
      console.log(`Exporting sequence "${sequence.name}" as JSON`);
      const exportData = {
        ...sequence,
        exportedAt: (/* @__PURE__ */ new Date()).toISOString(),
        exportedBy: "TKA V2 Modern",
        version: "2.0.0"
      };
      return JSON.stringify(exportData, null, 2);
    } catch (error) {
      console.error("Failed to export sequence as JSON:", error);
      throw new Error(
        `JSON export failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Render beat placeholder on canvas
   */
  async renderBeatPlaceholder(ctx, beat, x, y, size) {
    ctx.strokeStyle = "#e5e7eb";
    ctx.lineWidth = 2;
    ctx.strokeRect(x, y, size, size);
    ctx.fillStyle = "#374151";
    ctx.font = "16px monospace";
    ctx.textAlign = "center";
    ctx.fillText(String(beat.beat_number), x + size / 2, y + size / 2 + 6);
    const blueMotion = beat.pictograph_data?.motions?.blue;
    if (blueMotion) {
      ctx.fillStyle = "#3b82f6";
      ctx.fillRect(x + 5, y + 5, 10, 10);
    }
    const redMotion = beat.pictograph_data?.motions?.red;
    if (redMotion) {
      ctx.fillStyle = "#ef4444";
      ctx.fillRect(x + size - 15, y + 5, 10, 10);
    }
  }
  /**
   * Render title on canvas
   */
  renderTitle(ctx, title, canvasWidth) {
    ctx.fillStyle = "#111827";
    ctx.font = "bold 24px system-ui";
    ctx.textAlign = "center";
    ctx.fillText(title, canvasWidth / 2, 30);
  }
  /**
   * Get default export options
   */
  getDefaultExportOptions() {
    return {
      // Image settings
      quality: "medium",
      format: "PNG",
      resolution: "300",
      // Content options
      includeTitle: true,
      includeMetadata: false,
      includeBeatNumbers: true,
      includeAuthor: false,
      includeDifficulty: true,
      includeDate: false,
      includeStartPosition: true,
      includeReversalSymbols: true,
      // Layout options
      beatSize: 150,
      spacing: 10,
      padding: 20,
      // Compression settings
      pngCompression: 6,
      jpgQuality: 85
    };
  }
}
class LocalStoragePersistenceService {
  SEQUENCES_KEY = "tka-v2-sequences";
  SEQUENCE_PREFIX = "tka-v2-sequence-";
  /**
   * Save a sequence to localStorage
   */
  async saveSequence(sequence) {
    try {
      const sequenceKey = `${this.SEQUENCE_PREFIX}${sequence.id}`;
      localStorage.setItem(sequenceKey, JSON.stringify(sequence));
      await this.updateSequenceIndex(sequence);
      console.log(`Sequence "${sequence.name}" saved successfully`);
    } catch (error) {
      console.error("Failed to save sequence:", error);
      throw new Error(
        `Failed to save sequence: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Load a sequence by ID
   */
  async loadSequence(id) {
    try {
      const sequenceKey = `${this.SEQUENCE_PREFIX}${id}`;
      const data = localStorage.getItem(sequenceKey);
      if (!data) {
        return null;
      }
      const sequence = JSON.parse(data);
      return this.validateSequenceData(sequence);
    } catch (error) {
      console.error(`Failed to load sequence ${id}:`, error);
      return null;
    }
  }
  /**
   * Load all sequences
   */
  async loadAllSequences() {
    try {
      const indexData = localStorage.getItem(this.SEQUENCES_KEY);
      if (!indexData) {
        return [];
      }
      const sequenceIds = JSON.parse(indexData);
      const sequences = [];
      for (const id of sequenceIds) {
        const sequence = await this.loadSequence(id);
        if (sequence) {
          sequences.push(sequence);
        }
      }
      return sequences.sort((a, b) => {
        const aDate = new Date(a.metadata?.saved_at || 0).getTime();
        const bDate = new Date(b.metadata?.saved_at || 0).getTime();
        return bDate - aDate;
      });
    } catch (error) {
      console.error("Failed to load sequences:", error);
      return [];
    }
  }
  /**
   * Delete a sequence
   */
  async deleteSequence(id) {
    try {
      const sequenceKey = `${this.SEQUENCE_PREFIX}${id}`;
      localStorage.removeItem(sequenceKey);
      await this.removeFromSequenceIndex(id);
      console.log(`Sequence ${id} deleted successfully`);
    } catch (error) {
      console.error(`Failed to delete sequence ${id}:`, error);
      throw new Error(
        `Failed to delete sequence: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Update the sequence index with a new or updated sequence
   */
  async updateSequenceIndex(sequence) {
    try {
      const indexData = localStorage.getItem(this.SEQUENCES_KEY);
      const sequenceIds = indexData ? JSON.parse(indexData) : [];
      if (!sequenceIds.includes(sequence.id)) {
        sequenceIds.push(sequence.id);
        localStorage.setItem(this.SEQUENCES_KEY, JSON.stringify(sequenceIds));
      }
    } catch (error) {
      console.error("Failed to update sequence index:", error);
    }
  }
  /**
   * Remove a sequence ID from the index
   */
  async removeFromSequenceIndex(id) {
    try {
      const indexData = localStorage.getItem(this.SEQUENCES_KEY);
      if (!indexData) return;
      const sequenceIds = JSON.parse(indexData);
      const filteredIds = sequenceIds.filter((existingId) => existingId !== id);
      localStorage.setItem(this.SEQUENCES_KEY, JSON.stringify(filteredIds));
    } catch (error) {
      console.error("Failed to remove from sequence index:", error);
    }
  }
  /**
   * Validate sequence data structure
   */
  validateSequenceData(raw) {
    const data = raw || {};
    if (typeof data.id !== "string" || typeof data.name !== "string" || !Array.isArray(data.beats)) {
      throw new Error("Invalid sequence data structure");
    }
    const nowIso = (/* @__PURE__ */ new Date()).toISOString();
    const existingMeta = data.metadata || {};
    const metadata = {
      ...existingMeta,
      saved_at: typeof existingMeta.saved_at === "string" ? existingMeta.saved_at : nowIso,
      updated_at: nowIso
    };
    const beatsArray = Array.isArray(data.beats) ? data.beats : [];
    const beats = beatsArray.filter((b) => {
      if (b == null || typeof b !== "object") return false;
      const candidate = b;
      return "beat_number" in candidate;
    });
    const result = {
      id: data.id,
      name: data.name,
      beats,
      word: data.word || "",
      thumbnails: data.thumbnails || [],
      is_favorite: Boolean(data.is_favorite),
      is_circular: Boolean(data.is_circular),
      tags: data.tags || [],
      metadata,
      // **CRITICAL: Include start_position field if it exists**
      ...data.start_position ? { start_position: data.start_position } : {}
    };
    return result;
  }
  /**
   * Get storage usage statistics
   */
  getStorageInfo() {
    try {
      let used = 0;
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key?.startsWith("tka-v2-")) {
          const value = localStorage.getItem(key);
          used += (key.length + (value?.length || 0)) * 2;
        }
      }
      const indexData = localStorage.getItem(this.SEQUENCES_KEY);
      const sequenceCount = indexData ? JSON.parse(indexData).length : 0;
      return {
        used: Math.round(used / 1024),
        // KB
        available: 5120,
        // Rough estimate of 5MB localStorage limit
        sequences: sequenceCount
      };
    } catch {
      return { used: 0, available: 5120, sequences: 0 };
    }
  }
}
class MotionGenerationService {
  /**
   * Generate a motion for a specific color
   */
  async generateMotion(color, _options, _previousBeats) {
    try {
      console.log(`Generating ${color} motion`);
      const motionTypes = [
        MotionType.PRO,
        MotionType.ANTI,
        MotionType.FLOAT,
        MotionType.DASH,
        MotionType.STATIC
      ];
      const locations = [
        Location.NORTH,
        Location.EAST,
        Location.SOUTH,
        Location.WEST,
        Location.NORTHEAST,
        Location.SOUTHEAST,
        Location.SOUTHWEST,
        Location.NORTHWEST
      ];
      const orientations = [
        Orientation.IN,
        Orientation.OUT,
        Orientation.CLOCK,
        Orientation.COUNTER
      ];
      const rotationDirections = [
        RotationDirection.CLOCKWISE,
        RotationDirection.COUNTER_CLOCKWISE,
        RotationDirection.NO_ROTATION
      ];
      const motionType = this.randomChoice(motionTypes);
      const startLoc = this.randomChoice(locations);
      const endLoc = this.randomChoice(locations);
      const startOri = this.randomChoice(orientations);
      const endOri = this.randomChoice(orientations);
      const propRotDir = this.randomChoice(rotationDirections);
      const turns = this.calculateTurns(motionType, startLoc, endLoc);
      const motion = {
        motion_type: motionType,
        prop_rot_dir: propRotDir,
        start_loc: startLoc,
        end_loc: endLoc,
        turns,
        start_ori: startOri,
        end_ori: endOri,
        is_visible: true
      };
      console.log(`Generated ${color} motion:`, motion);
      return motion;
    } catch (error) {
      console.error(`Failed to generate ${color} motion:`, error);
      throw new Error(
        `Motion generation failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Calculate turns for a motion
   */
  calculateTurns(motionType, startLoc, endLoc) {
    if (motionType === "static") return 0;
    if (motionType === "dash") return 0;
    const locationOrder = ["n", "ne", "e", "se", "s", "sw", "w", "nw"];
    const startIndex = locationOrder.indexOf(startLoc);
    const endIndex = locationOrder.indexOf(endLoc);
    if (startIndex === -1 || endIndex === -1) return 1;
    const distance = Math.abs(endIndex - startIndex);
    return Math.min(distance, 8 - distance);
  }
  /**
   * Random choice helper
   */
  randomChoice(array) {
    if (array.length === 0) {
      throw new Error("randomChoice called with empty array");
    }
    return array[Math.floor(Math.random() * array.length)];
  }
  /**
   * Generate motion with constraints
   */
  async generateConstrainedMotion(color, options, previousBeats, _constraints) {
    return this.generateMotion(color, options, previousBeats);
  }
  /**
   * Validate if a motion is valid given the context
   */
  validateMotion(motion, _color, _previousBeats) {
    const reasons = [];
    if (!motion.motion_type) {
      reasons.push("Motion type is required");
    }
    if (!motion.start_loc) {
      reasons.push("Start location is required");
    }
    if (!motion.end_loc) {
      reasons.push("End location is required");
    }
    return {
      isValid: reasons.length === 0,
      reasons
    };
  }
}
function createMotionData(data = {}) {
  return {
    motion_type: data.motion_type ?? MotionType.STATIC,
    prop_rot_dir: data.prop_rot_dir ?? RotationDirection.NO_ROTATION,
    start_loc: data.start_loc ?? Location.NORTH,
    end_loc: data.end_loc ?? Location.NORTH,
    turns: data.turns ?? 0,
    start_ori: data.start_ori ?? Orientation.IN,
    end_ori: data.end_ori ?? Orientation.IN,
    is_visible: data.is_visible ?? true,
    prefloat_motion_type: data.prefloat_motion_type ?? null,
    prefloat_prop_rot_dir: data.prefloat_prop_rot_dir ?? null
  };
}
function createGridData$1(data = {}) {
  return {
    grid_mode: data.grid_mode ?? GridMode.DIAMOND,
    center_x: data.center_x ?? 0,
    center_y: data.center_y ?? 0,
    radius: data.radius ?? 100,
    grid_points: data.grid_points ?? {}
  };
}
function createArrowData(data = {}) {
  return {
    id: data.id ?? crypto.randomUUID(),
    arrow_type: data.arrow_type ?? ArrowType.BLUE,
    color: data.color ?? "blue",
    turns: data.turns ?? 0,
    is_mirrored: data.is_mirrored ?? false,
    motion_type: data.motion_type ?? "static",
    start_orientation: data.start_orientation ?? "in",
    end_orientation: data.end_orientation ?? "in",
    rotation_direction: data.rotation_direction ?? "clockwise",
    location: data.location ?? null,
    position_x: data.position_x ?? 0,
    position_y: data.position_y ?? 0,
    rotation_angle: data.rotation_angle ?? 0,
    coordinates: data.coordinates ?? null,
    svg_center: data.svg_center ?? null,
    svg_mirrored: data.svg_mirrored ?? false,
    is_visible: data.is_visible ?? true,
    is_selected: data.is_selected ?? false
  };
}
function createPropData(data = {}) {
  return {
    id: data.id ?? crypto.randomUUID(),
    prop_type: data.prop_type ?? PropType.STAFF,
    color: data.color ?? "blue",
    orientation: data.orientation ?? Orientation.IN,
    rotation_direction: data.rotation_direction ?? RotationDirection.NO_ROTATION,
    location: data.location ?? null,
    position_x: data.position_x ?? 0,
    position_y: data.position_y ?? 0,
    rotation_angle: data.rotation_angle ?? 0,
    coordinates: data.coordinates ?? null,
    svg_center: data.svg_center ?? null,
    is_visible: data.is_visible ?? true,
    is_selected: data.is_selected ?? false
  };
}
function createPictographData(data = {}) {
  const arrows = {
    blue: createArrowData({ arrow_type: ArrowType.BLUE, color: "blue" }),
    red: createArrowData({ arrow_type: ArrowType.RED, color: "red" }),
    ...data.arrows
  };
  const props = {
    blue: createPropData({ color: "blue" }),
    red: createPropData({ color: "red" }),
    ...data.props
  };
  return {
    id: data.id ?? crypto.randomUUID(),
    grid_data: data.grid_data ?? createGridData$1(),
    arrows,
    props,
    motions: data.motions ?? {},
    letter: data.letter ?? null,
    start_position: data.start_position ?? null,
    end_position: data.end_position ?? null,
    beat: data.beat ?? 0,
    timing: data.timing ?? null,
    direction: data.direction ?? null,
    duration: data.duration ?? null,
    letter_type: data.letter_type ?? null,
    is_blank: data.is_blank ?? false,
    is_mirrored: data.is_mirrored ?? false,
    metadata: data.metadata ?? {}
  };
}
function createBeatData(data = {}) {
  return {
    id: data.id ?? crypto.randomUUID(),
    beat_number: data.beat_number ?? 1,
    duration: data.duration ?? 1,
    blue_reversal: data.blue_reversal ?? false,
    red_reversal: data.red_reversal ?? false,
    is_blank: data.is_blank ?? false,
    pictograph_data: data.pictograph_data ?? null,
    metadata: data.metadata ?? {}
  };
}
var FilterType = /* @__PURE__ */ ((FilterType2) => {
  FilterType2["STARTING_LETTER"] = "starting_letter";
  FilterType2["CONTAINS_LETTERS"] = "contains_letters";
  FilterType2["LENGTH"] = "length";
  FilterType2["DIFFICULTY"] = "difficulty";
  FilterType2["STARTING_POSITION"] = "starting_position";
  FilterType2["AUTHOR"] = "author";
  FilterType2["GRID_MODE"] = "grid_mode";
  FilterType2["ALL_SEQUENCES"] = "all_sequences";
  FilterType2["FAVORITES"] = "favorites";
  FilterType2["RECENT"] = "recent";
  return FilterType2;
})(FilterType || {});
var SortMethod = /* @__PURE__ */ ((SortMethod2) => {
  SortMethod2["ALPHABETICAL"] = "alphabetical";
  SortMethod2["DATE_ADDED"] = "date_added";
  SortMethod2["DIFFICULTY_LEVEL"] = "difficulty_level";
  SortMethod2["SEQUENCE_LENGTH"] = "sequence_length";
  SortMethod2["AUTHOR"] = "author";
  SortMethod2["POPULARITY"] = "popularity";
  return SortMethod2;
})(SortMethod || {});
class CsvDataService {
  csvData = null;
  parsedData = null;
  isInitialized = false;
  constructor() {
  }
  /**
   * Load CSV data from multiple sources (global data or static files)
   */
  async loadCsvData() {
    if (this.isInitialized) {
      return;
    }
    try {
      if (typeof window !== "undefined" && window.csvData) {
        this.csvData = window.csvData;
      } else {
        const [diamondResponse, boxResponse] = await Promise.all([
          fetch("/DiamondPictographDataframe.csv"),
          fetch("/BoxPictographDataframe.csv")
        ]);
        if (!diamondResponse.ok || !boxResponse.ok) {
          throw new Error(
            `Failed to load CSV files: Diamond=${diamondResponse.status}, Box=${boxResponse.status}`
          );
        }
        const diamondData = await diamondResponse.text();
        const boxData = await boxResponse.text();
        this.csvData = { diamondData, boxData };
      }
      if (this.csvData) {
        this.parsedData = {
          [GridMode.DIAMOND]: this.parseCSV(this.csvData.diamondData),
          [GridMode.BOX]: this.parseCSV(this.csvData.boxData)
        };
      }
      this.isInitialized = true;
    } catch (error) {
      console.error("❌ Error loading CSV data:", error);
      throw new Error(
        `Failed to load CSV data: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Get CSV data (similar to legacy layout data)
   */
  getCsvData() {
    return this.csvData;
  }
  /**
   * Get parsed data for a specific grid mode
   */
  getParsedData(gridMode) {
    if (!this.parsedData) {
      return [];
    }
    return this.parsedData[gridMode];
  }
  /**
   * Get available options for a given end position (like legacy OptionDataService)
   */
  getNextOptions(endPosition, gridMode = GridMode.DIAMOND) {
    if (!this.parsedData) {
      return [];
    }
    try {
      const dataset = this.parsedData[gridMode];
      const matchingOptions = dataset.filter(
        (row) => row.startPos === endPosition
      );
      return matchingOptions;
    } catch (error) {
      console.error("❌ Error getting next options:", error);
      return [];
    }
  }
  /**
   * Parse CSV text into array of objects (same as legacy)
   */
  parseCSV(csvText) {
    const lines = csvText.trim().split("\n");
    if (lines.length < 2) return [];
    const headerLine = lines[0] ?? "";
    const headers = headerLine.split(",").map((h) => h.trim());
    const data = [];
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i] ?? "";
      const values = line.split(",").map((v) => v.trim());
      const row = {};
      headers.forEach((header, index) => {
        row[header] = values[index] || "";
      });
      data.push({
        letter: row.letter || "",
        startPos: row.startPos || "",
        endPos: row.endPos || "",
        timing: row.timing || "",
        direction: row.direction || "",
        blueMotionType: row.blueMotionType || "",
        bluePropRotDir: row.bluePropRotDir || "",
        blueStartLoc: row.blueStartLoc || "",
        blueEndLoc: row.blueEndLoc || "",
        redMotionType: row.redMotionType || "",
        redPropRotDir: row.redPropRotDir || "",
        redStartLoc: row.redStartLoc || "",
        redEndLoc: row.redEndLoc || ""
      });
    }
    return data;
  }
  /**
   * Get all available start positions for a given grid mode
   */
  getAvailableStartPositions(gridMode = GridMode.DIAMOND) {
    if (!this.parsedData) return [];
    const dataset = this.parsedData[gridMode];
    const startPositions = [...new Set(dataset.map((row) => row.startPos))];
    return startPositions.sort();
  }
  /**
   * Get all available end positions for a given grid mode
   */
  getAvailableEndPositions(gridMode = GridMode.DIAMOND) {
    if (!this.parsedData) return [];
    const dataset = this.parsedData[gridMode];
    const endPositions = [...new Set(dataset.map((row) => row.endPos))];
    return endPositions.sort();
  }
  /**
   * Get statistics about the loaded data
   */
  getDataStats() {
    if (!this.parsedData) return null;
    return {
      [GridMode.DIAMOND]: {
        total: this.parsedData.diamond.length,
        letters: [...new Set(this.parsedData.diamond.map((row) => row.letter))].length,
        startPositions: this.getAvailableStartPositions(GridMode.DIAMOND).length,
        endPositions: this.getAvailableEndPositions(GridMode.DIAMOND).length
      },
      [GridMode.BOX]: {
        total: this.parsedData.box.length,
        letters: [...new Set(this.parsedData.box.map((row) => row.letter))].length,
        startPositions: this.getAvailableStartPositions(GridMode.BOX).length,
        endPositions: this.getAvailableEndPositions(GridMode.BOX).length
      }
    };
  }
  /**
   * Check if the service is initialized
   */
  isReady() {
    return this.isInitialized && this.parsedData !== null;
  }
  /**
   * Debug method to inspect specific position data
   */
  debugPosition(_position, gridMode = GridMode.DIAMOND) {
    if (!this.parsedData) {
      return;
    }
    void this.parsedData[gridMode];
  }
}
class OrientationCalculationService {
  /**
   * Calculate end orientation for a motion based on motion type, turns, and start orientation
   */
  calculateEndOrientation(motion) {
    if (motion.motion_type === MotionType.FLOAT) {
      return this.calculateFloatOrientation(motion);
    }
    if (motion.turns === "fl") {
      return motion.start_ori;
    }
    const validTurns = [0, 0.5, 1, 1.5, 2, 2.5, 3];
    if (!validTurns.includes(motion.turns)) {
      console.warn(
        `Invalid turns value: ${motion.turns}. Using start orientation.`
      );
      return motion.start_ori;
    }
    if (motion.turns % 1 === 0) {
      return this.calculateWholeTurnOrientation(
        motion.motion_type,
        motion.turns,
        motion.start_ori
      );
    } else {
      return this.calculateHalfTurnOrientation(
        motion.motion_type,
        motion.turns,
        motion.start_ori,
        motion.prop_rot_dir
      );
    }
  }
  /**
   * Switch orientation between complementary pairs
   */
  switchOrientation(orientation) {
    const orientationMap = {
      [Orientation.IN]: Orientation.OUT,
      [Orientation.OUT]: Orientation.IN,
      [Orientation.CLOCK]: Orientation.COUNTER,
      [Orientation.COUNTER]: Orientation.CLOCK
    };
    return orientationMap[orientation] || orientation;
  }
  /**
   * Calculate orientation for whole turns (0, 1, 2, 3)
   */
  calculateWholeTurnOrientation(motionType, turns, startOri) {
    if (motionType === MotionType.PRO || motionType === MotionType.STATIC) {
      return turns % 2 === 0 ? startOri : this.switchOrientation(startOri);
    } else if (motionType === MotionType.ANTI || motionType === MotionType.DASH) {
      return turns % 2 === 0 ? this.switchOrientation(startOri) : startOri;
    }
    return startOri;
  }
  /**
   * Calculate orientation for half turns (0.5, 1.5, 2.5)
   */
  calculateHalfTurnOrientation(motionType, turns, startOri, propRotDir) {
    const rotDir = propRotDir === RotationDirection.CLOCKWISE ? "cw" : propRotDir === RotationDirection.COUNTER_CLOCKWISE ? "ccw" : "cw";
    let orientationMap;
    if (motionType === MotionType.ANTI || motionType === MotionType.DASH) {
      orientationMap = {
        [`${Orientation.IN}_cw`]: turns % 2 === 0.5 ? Orientation.CLOCK : Orientation.COUNTER,
        [`${Orientation.IN}_ccw`]: turns % 2 === 0.5 ? Orientation.COUNTER : Orientation.CLOCK,
        [`${Orientation.OUT}_cw`]: turns % 2 === 0.5 ? Orientation.COUNTER : Orientation.CLOCK,
        [`${Orientation.OUT}_ccw`]: turns % 2 === 0.5 ? Orientation.CLOCK : Orientation.COUNTER,
        [`${Orientation.CLOCK}_cw`]: turns % 2 === 0.5 ? Orientation.OUT : Orientation.IN,
        [`${Orientation.CLOCK}_ccw`]: turns % 2 === 0.5 ? Orientation.IN : Orientation.OUT,
        [`${Orientation.COUNTER}_cw`]: turns % 2 === 0.5 ? Orientation.IN : Orientation.OUT,
        [`${Orientation.COUNTER}_ccw`]: turns % 2 === 0.5 ? Orientation.OUT : Orientation.IN
      };
    } else if (motionType === MotionType.PRO || motionType === MotionType.STATIC) {
      orientationMap = {
        [`${Orientation.IN}_cw`]: turns % 2 === 0.5 ? Orientation.COUNTER : Orientation.CLOCK,
        [`${Orientation.IN}_ccw`]: turns % 2 === 0.5 ? Orientation.CLOCK : Orientation.COUNTER,
        [`${Orientation.OUT}_cw`]: turns % 2 === 0.5 ? Orientation.CLOCK : Orientation.COUNTER,
        [`${Orientation.OUT}_ccw`]: turns % 2 === 0.5 ? Orientation.COUNTER : Orientation.CLOCK,
        [`${Orientation.CLOCK}_cw`]: turns % 2 === 0.5 ? Orientation.IN : Orientation.OUT,
        [`${Orientation.CLOCK}_ccw`]: turns % 2 === 0.5 ? Orientation.OUT : Orientation.IN,
        [`${Orientation.COUNTER}_cw`]: turns % 2 === 0.5 ? Orientation.OUT : Orientation.IN,
        [`${Orientation.COUNTER}_ccw`]: turns % 2 === 0.5 ? Orientation.IN : Orientation.OUT
      };
    } else {
      return startOri;
    }
    const key = `${startOri}_${rotDir}`;
    return orientationMap[key] || startOri;
  }
  /**
   * Calculate orientation for float motions (simplified for now)
   * TODO: Implement proper handpath direction calculation
   */
  calculateFloatOrientation(motion) {
    console.log("🌊 Float orientation calculation (simplified)");
    return motion.start_ori;
  }
  /**
   * Create motion data with properly calculated end orientation
   */
  createMotionWithCalculatedOrientation(motionType, propRotDir, startLoc, endLoc, turns = 0, startOri = Orientation.IN) {
    const motion = {
      motion_type: motionType,
      prop_rot_dir: propRotDir,
      start_loc: startLoc,
      end_loc: endLoc,
      turns,
      start_ori: startOri,
      end_ori: startOri,
      // Will be calculated
      is_visible: true,
      prefloat_motion_type: null,
      prefloat_prop_rot_dir: null
    };
    return { ...motion, end_ori: this.calculateEndOrientation(motion) };
  }
}
class OptionDataService {
  MOTION_TYPES = [
    "pro",
    "anti",
    "float",
    "dash",
    "static"
  ];
  DIFFICULTY_MOTION_LIMITS = {
    beginner: { maxTurns: 1, allowedTypes: ["pro", "anti", "static"] },
    intermediate: {
      maxTurns: 2,
      allowedTypes: ["pro", "anti", "float", "static"]
    },
    advanced: {
      maxTurns: 3,
      allowedTypes: ["pro", "anti", "float", "dash", "static"]
    }
  };
  csvDataService;
  orientationCalculationService;
  constructor() {
    this.csvDataService = new CsvDataService();
    this.orientationCalculationService = new OrientationCalculationService();
  }
  /**
   * Initialize the service by loading CSV data
   */
  async initialize() {
    await this.csvDataService.loadCsvData();
  }
  /**
   * Get next options based on end position from CSV data (like legacy)
   */
  async getNextOptionsFromEndPosition(endPosition, gridMode = GridMode.DIAMOND, filters) {
    try {
      const csvOptions = this.csvDataService.getNextOptions(
        endPosition,
        gridMode
      );
      if (csvOptions.length === 0) {
        return [];
      }
      const pictographOptions = csvOptions.map(
        (row, index) => this.convertCsvRowToPictographDataInternal(row, gridMode, index)
      ).filter((option) => option !== null);
      let filteredOptions = pictographOptions;
      if (filters?.difficulty) {
        filteredOptions = this.filterOptionsByDifficulty(
          filteredOptions,
          filters.difficulty
        );
      }
      if (filters?.motionTypes) {
        filteredOptions = this.filterByMotionTypes(
          filteredOptions,
          filters.motionTypes
        );
      }
      if (filters?.minTurns !== void 0 || filters?.maxTurns !== void 0) {
        filteredOptions = this.filterByTurns(
          filteredOptions,
          filters.minTurns,
          filters.maxTurns
        );
      }
      return filteredOptions;
    } catch (error) {
      console.error("❌ Error getting options from CSV:", error);
      return [];
    }
  }
  async getNextOptions(currentSequence, filters) {
    try {
      const lastBeat = this.getLastBeat(currentSequence);
      if (!lastBeat?.pictograph_data) {
        return [];
      }
      const endPosition = this.extractEndPosition(lastBeat.pictograph_data);
      if (!endPosition) {
        return [];
      }
      const gridMode = lastBeat.pictograph_data.grid_data?.grid_mode === GridMode.BOX ? GridMode.BOX : GridMode.DIAMOND;
      return await this.getNextOptionsFromEndPosition(
        endPosition,
        gridMode,
        filters
      );
    } catch (error) {
      console.error("❌ Error generating options:", error);
      return [];
    }
  }
  filterOptionsByDifficulty(options, level) {
    const limits = this.DIFFICULTY_MOTION_LIMITS[level];
    const filtered = options.filter((option) => {
      if (option.motions?.blue) {
        const blueMotion = option.motions.blue;
        if (!limits.allowedTypes.includes(blueMotion.motion_type)) {
          return false;
        }
        if (typeof blueMotion.turns === "number" && blueMotion.turns > limits.maxTurns) {
          return false;
        }
      }
      if (option.motions?.red) {
        const redMotion = option.motions.red;
        if (!limits.allowedTypes.includes(redMotion.motion_type)) {
          return false;
        }
        if (typeof redMotion.turns === "number" && redMotion.turns > limits.maxTurns) {
          return false;
        }
      }
      return true;
    });
    return filtered;
  }
  validateOptionCompatibility(option, sequence) {
    const errors = [];
    if (!option.motions?.blue && !option.motions?.red) {
      errors.push({
        code: "MISSING_MOTION_DATA",
        message: "Option must have at least one motion",
        severity: "error"
      });
    }
    const lastBeat = this.getLastBeat(sequence);
    if (lastBeat?.pictograph_data) {
      const continuityErrors = this.validateMotionContinuity(
        lastBeat.pictograph_data,
        option
      );
      const validationErrors = continuityErrors.map((error) => ({
        code: "MOTION_CONTINUITY_ERROR",
        message: error,
        severity: "error"
      }));
      errors.push(...validationErrors);
    }
    return {
      isValid: errors.length === 0,
      errors,
      warnings: []
    };
  }
  getAvailableMotionTypes() {
    return [...this.MOTION_TYPES];
  }
  /**
   * Convert CSV row to PictographData format (public method for external use)
   */
  convertCsvRowToPictographData(row, gridMode, index = 0) {
    return this.convertCsvRowToPictographDataInternal(row, gridMode, index);
  }
  /**
   * Convert CSV row to PictographData format (based on legacy implementation)
   */
  convertCsvRowToPictographDataInternal(row, gridMode, index = 0) {
    try {
      const blueMotion = this.createMotionDataFromCsv(row, "blue");
      const redMotion = this.createMotionDataFromCsv(row, "red");
      const blueArrow = createArrowData({
        arrow_type: ArrowType.BLUE,
        color: "blue",
        turns: 0,
        // Will be set from motion data
        location: this.mapLocationString(row.blueStartLoc)
      });
      const redArrow = createArrowData({
        arrow_type: ArrowType.RED,
        color: "red",
        turns: 0,
        // Will be set from motion data
        location: this.mapLocationString(row.redStartLoc)
      });
      const blueProp = createPropData({
        prop_type: PropType.STAFF,
        color: "blue",
        location: this.mapLocationString(row.blueEndLoc)
      });
      const redProp = createPropData({
        prop_type: PropType.STAFF,
        color: "red",
        location: this.mapLocationString(row.redEndLoc)
      });
      const pictograph = createPictographData({
        id: `${gridMode}-${row.letter || "unknown"}-${row.startPos || "unknown"}-${row.endPos || "unknown"}-${index}`,
        grid_data: createGridData$1({
          grid_mode: gridMode
        }),
        arrows: { blue: blueArrow, red: redArrow },
        props: { blue: blueProp, red: redProp },
        motions: { blue: blueMotion, red: redMotion },
        letter: row.letter,
        beat: 0,
        is_blank: false,
        is_mirrored: false
      });
      return pictograph;
    } catch (error) {
      console.error(
        "❌ Error converting CSV row to PictographData:",
        error,
        row
      );
      return null;
    }
  }
  /**
   * Create motion data from CSV row with proper orientation calculation
   */
  createMotionDataFromCsv(row, color) {
    const motionType = row[`${color}MotionType`];
    const propRotDir = row[`${color}PropRotDir`];
    const startLoc = row[`${color}StartLoc`];
    const endLoc = row[`${color}EndLoc`];
    const motion = this.orientationCalculationService.createMotionWithCalculatedOrientation(
      this.mapMotionType(motionType),
      this.mapRotationDirection(propRotDir),
      this.mapLocationString(startLoc),
      this.mapLocationString(endLoc),
      0,
      // Basic turns for now - could be enhanced to read from CSV
      Orientation.IN
      // Standard start orientation
    );
    return motion;
  }
  /**
   * Map string motion type to domain enum
   */
  mapMotionType(motionType) {
    switch (motionType.toLowerCase()) {
      case "pro":
        return MotionType.PRO;
      case "anti":
        return MotionType.ANTI;
      case "float":
        return MotionType.FLOAT;
      case "dash":
        return MotionType.DASH;
      case "static":
        return MotionType.STATIC;
      default:
        return MotionType.PRO;
    }
  }
  /**
   * Map string rotation direction to domain enum
   */
  mapRotationDirection(rotDir) {
    switch (rotDir.toLowerCase()) {
      case "cw":
        return RotationDirection.CLOCKWISE;
      case "ccw":
        return RotationDirection.COUNTER_CLOCKWISE;
      case "no_rot":
        return RotationDirection.NO_ROTATION;
      default:
        return RotationDirection.NO_ROTATION;
    }
  }
  /**
   * Map string location to domain enum
   */
  mapLocationString(loc) {
    switch (loc.toLowerCase()) {
      case "n":
        return Location.NORTH;
      case "s":
        return Location.SOUTH;
      case "e":
        return Location.EAST;
      case "w":
        return Location.WEST;
      case "ne":
        return Location.NORTHEAST;
      case "se":
        return Location.SOUTHEAST;
      case "sw":
        return Location.SOUTHWEST;
      case "nw":
        return Location.NORTHWEST;
      default:
        return Location.SOUTH;
    }
  }
  getLastBeat(sequence) {
    if (!sequence.beats || sequence.beats.length === 0) {
      return null;
    }
    return sequence.beats[sequence.beats.length - 1] ?? null;
  }
  /**
   * Extract end position from pictograph data
   */
  extractEndPosition(pictographData) {
    const blueEnd = pictographData.motions?.blue?.end_loc;
    if (blueEnd) return this.mapLocationToPositionString(blueEnd);
    const redEnd = pictographData.motions?.red?.end_loc;
    if (redEnd) return this.mapLocationToPositionString(redEnd);
    return null;
  }
  /**
   * Map location enum to position string
   */
  mapLocationToPositionString(_location) {
    return "alpha1";
  }
  filterByMotionTypes(options, motionTypes) {
    return options.filter((option) => {
      const blueValid = !option.motions?.blue || motionTypes.includes(
        option.motions.blue.motion_type
      );
      const redValid = !option.motions?.red || motionTypes.includes(
        option.motions.red.motion_type
      );
      return blueValid && redValid;
    });
  }
  filterByTurns(options, minTurns, maxTurns) {
    return options.filter((option) => {
      if (option.motions?.blue) {
        const blueTurns = typeof option.motions.blue.turns === "number" ? option.motions.blue.turns : 0;
        if (minTurns !== void 0 && blueTurns < minTurns) return false;
        if (maxTurns !== void 0 && blueTurns > maxTurns) return false;
      }
      if (option.motions?.red) {
        const redTurns = typeof option.motions.red.turns === "number" ? option.motions.red.turns : 0;
        if (minTurns !== void 0 && redTurns < minTurns) return false;
        if (maxTurns !== void 0 && redTurns > maxTurns) return false;
      }
      return true;
    });
  }
  validateMotionContinuity(lastPictograph, nextOption) {
    const errors = [];
    if (lastPictograph.motions?.blue && nextOption.motions?.blue) {
      lastPictograph.motions.blue?.end_loc;
      nextOption.motions.blue?.start_loc;
    }
    if (lastPictograph.motions?.red && nextOption.motions?.red) {
      lastPictograph.motions.red?.end_loc;
      nextOption.motions.red?.start_loc;
    }
    return errors;
  }
}
class PanelManagementService {
  panels = /* @__PURE__ */ new Map();
  configurations = /* @__PURE__ */ new Map();
  currentResize = null;
  stateChangeCallbacks = [];
  constructor() {
    this.loadPanelStates();
  }
  // Panel registration
  registerPanel(config) {
    this.configurations.set(config.id, config);
    if (!this.panels.has(config.id)) {
      const savedWidth = this.loadPanelWidth(
        config.persistKey,
        config.defaultWidth
      );
      const initialState = {
        id: config.id,
        width: savedWidth,
        isCollapsed: false,
        isVisible: true,
        minWidth: config.minWidth,
        maxWidth: config.maxWidth,
        defaultWidth: config.defaultWidth,
        collapsedWidth: config.collapsedWidth,
        isResizing: false
      };
      this.panels.set(config.id, initialState);
    }
  }
  unregisterPanel(panelId) {
    this.panels.delete(panelId);
    this.configurations.delete(panelId);
  }
  // Panel state management
  getPanelState(panelId) {
    const state = this.panels.get(panelId);
    if (!state) {
      console.warn(`Panel not registered: ${panelId}, returning default state`);
      return {
        id: panelId,
        width: 300,
        isCollapsed: false,
        isVisible: true,
        minWidth: 200,
        maxWidth: 600,
        defaultWidth: 300,
        collapsedWidth: 60,
        isResizing: false
      };
    }
    return { ...state };
  }
  togglePanelCollapse(panelId) {
    const state = this.panels.get(panelId);
    if (!state) return;
    this.setPanelCollapsed(panelId, !state.isCollapsed);
  }
  setPanelCollapsed(panelId, isCollapsed) {
    const state = this.panels.get(panelId);
    if (!state) return;
    const updatedState = {
      ...state,
      isCollapsed
      // Don't change width when collapsing - layout handles this with CSS
    };
    this.panels.set(panelId, updatedState);
    this.notifyStateChange(panelId, updatedState);
    this.savePanelStates();
  }
  setPanelVisible(panelId, isVisible) {
    const state = this.panels.get(panelId);
    if (!state) return;
    const updatedState = {
      ...state,
      isVisible
    };
    this.panels.set(panelId, updatedState);
    this.notifyStateChange(panelId, updatedState);
  }
  setPanelWidth(panelId, width) {
    const state = this.panels.get(panelId);
    if (!state) return;
    const validatedWidth = this.validateWidth(panelId, width);
    const updatedState = {
      ...state,
      width: validatedWidth
    };
    this.panels.set(panelId, updatedState);
    this.notifyStateChange(panelId, updatedState);
    this.savePanelStates();
  }
  // Resize operations
  startResize(panelId, startX) {
    const state = this.panels.get(panelId);
    if (!state || !this.canResize(panelId)) {
      return null;
    }
    const operation = {
      panelId,
      startWidth: state.width,
      startX,
      currentX: startX
    };
    this.currentResize = operation;
    const updatedState = { ...state, isResizing: true };
    this.panels.set(panelId, updatedState);
    this.notifyStateChange(panelId, updatedState);
    return operation;
  }
  updateResize(operation, currentX) {
    const state = this.panels.get(operation.panelId);
    if (!state) {
      throw new Error(`Panel not found during resize: ${operation.panelId}`);
    }
    operation.currentX = currentX;
    const deltaX = currentX - operation.startX;
    const newWidth = operation.startWidth + deltaX;
    const validatedWidth = this.validateWidth(operation.panelId, newWidth);
    const updatedState = {
      ...state,
      width: validatedWidth
    };
    this.panels.set(operation.panelId, updatedState);
    this.notifyStateChange(operation.panelId, updatedState);
    return updatedState;
  }
  endResize(operation) {
    const state = this.panels.get(operation.panelId);
    if (!state) return;
    const updatedState = { ...state, isResizing: false };
    this.panels.set(operation.panelId, updatedState);
    this.notifyStateChange(operation.panelId, updatedState);
    this.currentResize = null;
    this.savePanelStates();
  }
  // Validation
  validateWidth(panelId, width) {
    const state = this.panels.get(panelId);
    if (!state) return width;
    return Math.max(state.minWidth, Math.min(state.maxWidth, width));
  }
  canResize(panelId) {
    const state = this.panels.get(panelId);
    return !!(state && state.isVisible && !state.isCollapsed);
  }
  // Persistence
  savePanelStates() {
    try {
      const states = {};
      for (const [panelId, state] of this.panels) {
        const config = this.configurations.get(panelId);
        if (config) {
          states[config.persistKey] = {
            width: state.width,
            isCollapsed: state.isCollapsed
          };
        }
      }
      localStorage.setItem("tka-panel-states", JSON.stringify(states));
    } catch (error) {
      console.warn("Failed to save panel states:", error);
    }
  }
  loadPanelStates() {
    try {
      const saved = localStorage.getItem("tka-panel-states");
      if (!saved) return;
      const states = JSON.parse(saved);
      this.savedStates = states;
    } catch (error) {
      console.warn("Failed to load panel states:", error);
    }
  }
  savedStates = {};
  loadPanelWidth(persistKey, defaultWidth) {
    const saved = this.savedStates[persistKey];
    return saved?.width ?? defaultWidth;
  }
  loadPanelCollapsed(persistKey) {
    const saved = this.savedStates[persistKey];
    return saved?.isCollapsed ?? false;
  }
  // Event handling
  onPanelStateChanged(callback) {
    this.stateChangeCallbacks.push(callback);
  }
  offPanelStateChanged(callback) {
    const index = this.stateChangeCallbacks.indexOf(callback);
    if (index > -1) {
      this.stateChangeCallbacks.splice(index, 1);
    }
  }
  notifyStateChange(panelId, state) {
    this.stateChangeCallbacks.forEach((callback) => {
      try {
        callback(panelId, { ...state });
      } catch (error) {
        console.error("Error in panel state change callback:", error);
      }
    });
  }
  // Utility methods
  getAllPanelStates() {
    const states = {};
    for (const [panelId, state] of this.panels) {
      states[panelId] = { ...state };
    }
    return states;
  }
  resetPanel(panelId) {
    const config = this.configurations.get(panelId);
    if (!config) return;
    const resetState = {
      id: panelId,
      width: config.defaultWidth,
      isCollapsed: false,
      isVisible: true,
      minWidth: config.minWidth,
      maxWidth: config.maxWidth,
      defaultWidth: config.defaultWidth,
      collapsedWidth: config.collapsedWidth,
      isResizing: false
    };
    this.panels.set(panelId, resetState);
    this.notifyStateChange(panelId, resetState);
    this.savePanelStates();
  }
  resetAllPanels() {
    for (const panelId of this.panels.keys()) {
      this.resetPanel(panelId);
    }
  }
}
const LETTER_CLASSIFICATIONS = {
  Type1: [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V"
  ],
  Type2: ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"],
  Type3: ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"],
  Type4: ["Φ", "Ψ", "Λ"],
  Type5: ["Φ-", "Ψ-", "Λ-"],
  Type6: ["α", "β", "Γ"]
};
function getLetterType(letter) {
  if (!letter) return "Type1";
  for (const [type, letters] of Object.entries(LETTER_CLASSIFICATIONS)) {
    if (letters.includes(letter)) {
      return type;
    }
  }
  return "Type1";
}
function getLetterFilename(letter) {
  return letter;
}
function getLetterImagePath(letter) {
  const letterType = getLetterType(letter);
  const filename = getLetterFilename(letter);
  const encodedFilename = encodeURIComponent(filename);
  return `/images/letters_trimmed/${letterType}/${encodedFilename}.svg`;
}
const gridCoordinates = {
  diamond: {
    hand_points: {
      normal: {
        n_diamond_hand_point: "(475.0, 331.9)",
        e_diamond_hand_point: "(618.1, 475.0)",
        s_diamond_hand_point: "(475.0, 618.1)",
        w_diamond_hand_point: "(331.9, 475.0)"
      },
      strict: {
        n_diamond_hand_point_strict: "(475.0, 325.0)",
        e_diamond_hand_point_strict: "(625.0, 475.0)",
        s_diamond_hand_point_strict: "(475.0, 625.0)",
        w_diamond_hand_point_strict: "(325.0, 475.0)"
      }
    },
    layer2_points: {
      normal: {
        ne_diamond_layer2_point: "(618.1, 331.9)",
        se_diamond_layer2_point: "(618.1, 618.1)",
        sw_diamond_layer2_point: "(331.9, 618.1)",
        nw_diamond_layer2_point: "(331.9, 331.9)"
      },
      strict: {
        ne_diamond_layer2_point_strict: "(625.0, 325.0)",
        se_diamond_layer2_point_strict: "(625.0, 625.0)",
        sw_diamond_layer2_point_strict: "(325.0, 625.0)",
        nw_diamond_layer2_point_strict: "(325.0, 325.0)"
      }
    },
    outer_points: {
      n_diamond_outer_point: "(475, 175)",
      e_diamond_outer_point: "(775, 475)",
      s_diamond_outer_point: "(475, 775)",
      w_diamond_outer_point: "(175, 475)"
    },
    center_point: "(475.0, 475.0)"
  },
  box: {
    hand_points: {
      normal: {
        ne_box_hand_point: "(576.2, 373.8)",
        se_box_hand_point: "(576.2, 576.2)",
        sw_box_hand_point: "(373.8, 576.2)",
        nw_box_hand_point: "(373.8, 373.8)"
      },
      strict: {
        ne_box_hand_point_strict: "(581.1, 368.9)",
        se_box_hand_point_strict: "(581.1, 581.1)",
        sw_box_hand_point_strict: "(368.9, 581.1)",
        nw_box_hand_point_strict: "(368.9, 368.9)"
      }
    },
    layer2_points: {
      normal: {
        n_box_layer2_point: "(475, 272.6)",
        e_box_layer2_point: "(677.4, 475)",
        s_box_layer2_point: "(475, 677.4)",
        w_box_layer2_point: "(272.6, 475)"
      },
      strict: {
        n_box_layer2_point_strict: "(475, 262.9)",
        e_box_layer2_point_strict: "(687.1, 475)",
        s_box_layer2_point_strict: "(475, 687.1)",
        w_box_layer2_point_strict: "(262.9, 475)"
      }
    },
    outer_points: {
      ne_box_outer_point: "(262.9, 247.9)",
      se_box_outer_point: "(687.1, 247.9)",
      sw_box_outer_point: "(687.1, 672.1)",
      nw_box_outer_point: "(262.9, 672.1)"
    },
    center_point: "(475.0, 475.0)"
  }
};
function parseCoordinates(coordString) {
  if (!coordString || coordString === "None") return null;
  try {
    const parts = coordString.replace(/[()]/g, "").split(", ").map(parseFloat);
    if (parts.length !== 2) {
      console.error(`Invalid coordinate format: "${coordString}"`);
      return null;
    }
    const [x, y] = parts;
    if (x === void 0 || y === void 0 || isNaN(x) || isNaN(y)) {
      console.error(`Invalid coordinates parsed: "${coordString}"`);
      return null;
    }
    return { x, y };
  } catch (error) {
    console.error(`Failed to parse coordinates: "${coordString}"`, error);
    return null;
  }
}
function createGridData(mode) {
  const modeData = gridCoordinates[mode];
  const parsePoints = (points) => Object.fromEntries(
    Object.entries(points).map(([key, value]) => [
      key,
      { coordinates: parseCoordinates(value) }
    ])
  );
  return {
    allHandPointsStrict: parsePoints(modeData.hand_points.strict),
    allHandPointsNormal: parsePoints(modeData.hand_points.normal),
    allLayer2PointsStrict: parsePoints(modeData.layer2_points.strict),
    allLayer2PointsNormal: parsePoints(modeData.layer2_points.normal),
    allOuterPoints: parsePoints(modeData.outer_points),
    centerPoint: { coordinates: parseCoordinates(modeData.center_point) }
  };
}
class PictographRenderingService {
  constructor(arrowPositioning, _propRendering) {
    this.arrowPositioning = arrowPositioning;
  }
  SVG_SIZE = 950;
  CENTER_X = 475;
  CENTER_Y = 475;
  /**
   * Render a pictograph from pictograph data
   */
  async renderPictograph(data) {
    try {
      const svg = this.createBaseSVG();
      const gridMode = data.grid_data?.grid_mode ?? GridMode.DIAMOND;
      await this.renderGrid(svg, gridMode);
      const rawGridData = createGridData(gridMode);
      const gridDataWithMode = this.adaptGridData(rawGridData, gridMode);
      const arrowPositions = await this.arrowPositioning.calculateAllArrowPositions(
        data,
        gridDataWithMode
      );
      for (const [color, position] of arrowPositions.entries()) {
        const motionData = data.motions?.[color];
        await this.renderArrowAtPosition(
          svg,
          color,
          position,
          motionData
        );
      }
      await this.renderProps(svg, data);
      await this.renderOverlays(svg, data);
      this.renderIdLabel(svg, data);
      this.renderDebugInfo(svg, data, arrowPositions);
      return svg;
    } catch (error) {
      console.error("❌ Error rendering pictograph:", error);
      const errorMessage = error instanceof Error ? error.message : "Unknown error";
      return this.createErrorSVG(errorMessage);
    }
  }
  /** Render glyph overlays (letters now; VTG/elemental when data is available) */
  async renderOverlays(svg, data) {
    try {
      if (data.letter) {
        await this.renderLetterGlyph(svg, data.letter);
      }
    } catch {
    }
  }
  async renderLetterGlyph(svg, letter) {
    const path = getLetterImagePath(letter);
    if (!path) return;
    const res = await fetch(path);
    if (!res.ok) return;
    const content = await res.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(content, "image/svg+xml");
    const el = doc.documentElement;
    const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
    group.setAttribute("class", "tka-letter");
    group.setAttribute("opacity", "0");
    const imported = document.importNode(el, true);
    group.appendChild(imported);
    svg.appendChild(group);
    let bbox;
    try {
      bbox = group.getBBox();
    } catch {
      bbox = new DOMRect(0, 0, 120, 80);
    }
    const letterHeight = bbox.height || 80;
    const x = Math.round(letterHeight / 1.5);
    const y = Math.round(this.SVG_SIZE - letterHeight * 1.7);
    group.setAttribute("transform", `translate(${x}, ${y})`);
    group.removeAttribute("opacity");
  }
  // Removed legacy glyph rendering helpers (vtg/elemental)
  /**
   * Render a beat as a pictograph
   */
  async renderBeat(beat) {
    const pictographData = this.beatToPictographData(beat);
    const svg = await this.renderPictograph(pictographData);
    return svg;
  }
  /**
   * Create base SVG element
   */
  createBaseSVG() {
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("width", this.SVG_SIZE.toString());
    svg.setAttribute("height", this.SVG_SIZE.toString());
    svg.setAttribute("viewBox", `0 0 ${this.SVG_SIZE} ${this.SVG_SIZE}`);
    svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    const background = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "rect"
    );
    background.setAttribute("width", "100%");
    background.setAttribute("height", "100%");
    background.setAttribute("fill", "#ffffff");
    svg.appendChild(background);
    return svg;
  }
  /**
   * Adapt raw grid data to match the interface requirements
   */
  adaptGridData(rawGridData, mode) {
    const adaptPoints = (points) => {
      const adapted = {};
      for (const [key, point] of Object.entries(points)) {
        if (point.coordinates) {
          adapted[key] = { coordinates: point.coordinates };
        }
      }
      return adapted;
    };
    return {
      mode,
      allLayer2PointsNormal: adaptPoints(
        rawGridData.allLayer2PointsNormal || {}
      ),
      allHandPointsNormal: adaptPoints(rawGridData.allHandPointsNormal || {})
    };
  }
  /**
   * Render arrow at sophisticated calculated position using real SVG assets
   */
  async renderArrowAtPosition(svg, color, position, motionData) {
    try {
      const arrowSvgPath = this.getArrowSvgPath(motionData);
      const response = await fetch(arrowSvgPath);
      if (!response.ok) {
        throw new Error(`Failed to load arrow SVG: ${response.status}`);
      }
      const svgContent = await response.text();
      const arrowGroup = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "g"
      );
      arrowGroup.setAttribute(
        "class",
        `arrow-${color} sophisticated-positioning`
      );
      arrowGroup.setAttribute("data-color", color);
      arrowGroup.setAttribute("data-position", `${position.x},${position.y}`);
      arrowGroup.setAttribute("data-rotation", position.rotation.toString());
      const transform = `translate(${position.x}, ${position.y}) rotate(${position.rotation})`;
      arrowGroup.setAttribute("transform", transform);
      const parser = new DOMParser();
      const svgDoc = parser.parseFromString(svgContent, "image/svg+xml");
      const svgElement = svgDoc.documentElement;
      this.applyArrowColorTransformation(svgElement, color);
      const importedSvg = document.importNode(svgElement, true);
      arrowGroup.appendChild(importedSvg);
      svg.appendChild(arrowGroup);
    } catch (error) {
      console.error(`❌ Error loading arrow SVG for ${color}:`, error);
      this.renderFallbackArrow(svg, color, position);
    }
  }
  /**
   * Get the correct arrow SVG path based on motion data (like ArrowSvgManager)
   */
  getArrowSvgPath(motionData) {
    if (!motionData) {
      return "/images/arrows/static/from_radial/static_0.svg";
    }
    const motionType = motionData.motion_type;
    const turnsVal = motionData.turns;
    const startOri = motionData.start_ori;
    if (motionType === "float") return "/images/arrows/float.svg";
    const radialPath = startOri === "in" ? "from_radial" : "from_nonradial";
    let turnsStr;
    if (turnsVal === "fl") {
      turnsStr = "fl";
    } else if (typeof turnsVal === "number") {
      turnsStr = turnsVal % 1 === 0 ? `${turnsVal}.0` : turnsVal.toString();
    } else {
      turnsStr = "0.0";
    }
    return `/images/arrows/${motionType}/${radialPath}/${motionType}_${turnsStr}.svg`;
  }
  /**
   * Apply color transformation to arrow SVG
   */
  applyArrowColorTransformation(svgElement, color) {
    const paths = svgElement.querySelectorAll("path");
    const fillColor = color === "blue" ? "#3b82f6" : "#ef4444";
    const strokeColor = color === "blue" ? "#1d4ed8" : "#dc2626";
    paths.forEach((path) => {
      path.setAttribute("fill", fillColor);
      path.setAttribute("stroke", strokeColor);
      path.setAttribute("stroke-width", "1");
    });
  }
  /**
   * Render fallback arrow if SVG loading fails
   */
  renderFallbackArrow(svg, color, position) {
    const arrowGroup = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "g"
    );
    arrowGroup.setAttribute("class", `arrow-${color} fallback`);
    arrowGroup.setAttribute(
      "transform",
      `translate(${position.x}, ${position.y}) rotate(${position.rotation})`
    );
    const arrowPath = this.createEnhancedArrowPath(color);
    arrowGroup.appendChild(arrowPath);
    svg.appendChild(arrowGroup);
  }
  /**
   * Create enhanced arrow SVG path with sophisticated styling
   */
  createEnhancedArrowPath(color) {
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", "M 0,-25 L 15,0 L 0,25 L -8,15 L -8,-15 Z");
    path.setAttribute("fill", color);
    path.setAttribute("stroke", "#000000");
    path.setAttribute("stroke-width", "2");
    path.setAttribute("opacity", "0.9");
    path.setAttribute("filter", "drop-shadow(1px 1px 2px rgba(0,0,0,0.3))");
    path.setAttribute("class", "sophisticated-arrow");
    return path;
  }
  /**
   * Render ID label with enhanced metadata
   */
  renderIdLabel(svg, data) {
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", this.CENTER_X.toString());
    text.setAttribute("y", (this.CENTER_Y + 130).toString());
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("font-family", "monospace");
    text.setAttribute("font-size", "11");
    text.setAttribute("fill", "#4b5563");
    text.textContent = `${data.id.slice(-8)} • Sophisticated Positioning`;
    svg.appendChild(text);
  }
  /**
   * Render debug information about positioning
   */
  renderDebugInfo(svg, data, positions) {
    let yOffset = 15;
    for (const [color, position] of positions.entries()) {
      const debugText = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "text"
      );
      debugText.setAttribute("x", "10");
      debugText.setAttribute("y", yOffset.toString());
      debugText.setAttribute("font-family", "monospace");
      debugText.setAttribute("font-size", "10");
      debugText.setAttribute("fill", "#6b7280");
      debugText.textContent = `${color}: [${position.x.toFixed(1)}, ${position.y.toFixed(1)}] ∠${position.rotation.toFixed(0)}°`;
      svg.appendChild(debugText);
      yOffset += 12;
    }
    if (data.letter) {
      const letterText = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "text"
      );
      letterText.setAttribute("x", "10");
      letterText.setAttribute("y", yOffset.toString());
      letterText.setAttribute("font-family", "monospace");
      letterText.setAttribute("font-size", "10");
      letterText.setAttribute("fill", "#059669");
      letterText.setAttribute("font-weight", "bold");
      letterText.textContent = `Letter: ${data.letter}`;
      svg.appendChild(letterText);
    }
  }
  /**
   * Render props for both colors
   * DISABLED: Props are now rendered by Prop.svelte components to avoid duplicates
   */
  async renderProps(_svg, _data) {
    return;
  }
  /**
   * Render grid using real SVG assets
   */
  async renderGrid(svg, gridMode = GridMode.DIAMOND) {
    try {
      const gridPath = `/images/grid/${gridMode}_grid.svg`;
      const gridImage = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "image"
      );
      gridImage.setAttribute("href", gridPath);
      gridImage.setAttribute("x", "0");
      gridImage.setAttribute("y", "0");
      gridImage.setAttribute("width", this.SVG_SIZE.toString());
      gridImage.setAttribute("height", this.SVG_SIZE.toString());
      gridImage.setAttribute("preserveAspectRatio", "none");
      svg.appendChild(gridImage);
    } catch (error) {
      console.error(`❌ Error loading grid SVG for ${gridMode} mode:`, error);
      this.renderFallbackGrid(svg, gridMode);
    }
  }
  /**
   * Fallback grid rendering if SVG loading fails
   */
  renderFallbackGrid(svg, gridMode) {
    const gridGroup = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "g"
    );
    gridGroup.setAttribute("class", `fallback-grid-${gridMode}`);
    if (gridMode === GridMode.DIAMOND) {
      const diamond = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "polygon"
      );
      const size = 143;
      const points = [
        `${this.CENTER_X},${this.CENTER_Y - size}`,
        // top
        `${this.CENTER_X + size},${this.CENTER_Y}`,
        // right
        `${this.CENTER_X},${this.CENTER_Y + size}`,
        // bottom
        `${this.CENTER_X - size},${this.CENTER_Y}`
        // left
      ].join(" ");
      diamond.setAttribute("points", points);
      diamond.setAttribute("fill", "none");
      diamond.setAttribute("stroke", "#e5e7eb");
      diamond.setAttribute("stroke-width", "2");
      gridGroup.appendChild(diamond);
    } else {
      const box = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "rect"
      );
      const size = 202;
      box.setAttribute("x", (this.CENTER_X - size / 2).toString());
      box.setAttribute("y", (this.CENTER_Y - size / 2).toString());
      box.setAttribute("width", size.toString());
      box.setAttribute("height", size.toString());
      box.setAttribute("fill", "none");
      box.setAttribute("stroke", "#e5e7eb");
      box.setAttribute("stroke-width", "2");
      gridGroup.appendChild(box);
    }
    svg.appendChild(gridGroup);
  }
  /**
   * Convert beat data to pictograph data
   */
  beatToPictographData(beat) {
    const motions = {};
    if (beat.pictograph_data?.motions?.blue)
      motions.blue = beat.pictograph_data.motions.blue;
    if (beat.pictograph_data?.motions?.red)
      motions.red = beat.pictograph_data.motions.red;
    return createPictographData({
      id: `beat-${beat.beat_number}`,
      grid_data: createGridData$1(),
      arrows: {
        blue: createArrowData({ arrow_type: ArrowType.BLUE, color: "blue" }),
        red: createArrowData({ arrow_type: ArrowType.RED, color: "red" })
      },
      props: {
        blue: createPropData({ prop_type: PropType.STAFF, color: "blue" }),
        red: createPropData({ prop_type: PropType.STAFF, color: "red" })
      },
      motions,
      letter: beat.pictograph_data?.letter || null,
      beat: beat.beat_number,
      is_blank: beat.is_blank,
      is_mirrored: false
    });
  }
  /**
   * Create error SVG with detailed error information
   */
  createErrorSVG(errorMessage) {
    const svg = this.createBaseSVG();
    const errorText = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "text"
    );
    errorText.setAttribute("x", this.CENTER_X.toString());
    errorText.setAttribute("y", this.CENTER_Y.toString());
    errorText.setAttribute("text-anchor", "middle");
    errorText.setAttribute("fill", "#dc2626");
    errorText.setAttribute("font-weight", "bold");
    errorText.textContent = "Rendering Error";
    if (errorMessage) {
      const detailText = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "text"
      );
      detailText.setAttribute("x", this.CENTER_X.toString());
      detailText.setAttribute("y", (this.CENTER_Y + 20).toString());
      detailText.setAttribute("text-anchor", "middle");
      detailText.setAttribute("fill", "#dc2626");
      detailText.setAttribute("font-size", "12");
      detailText.textContent = errorMessage.substring(0, 50) + (errorMessage.length > 50 ? "..." : "");
      svg.appendChild(detailText);
    }
    svg.appendChild(errorText);
    return svg;
  }
}
class PictographService {
  constructor(renderingService) {
    this.renderingService = renderingService;
  }
  /**
   * Render a pictograph to SVG
   */
  async renderPictograph(data) {
    try {
      return await this.renderingService.renderPictograph(data);
    } catch (error) {
      console.error("Failed to render pictograph:", error);
      return this.createFallbackSVG();
    }
  }
  /**
   * Update arrow data in a pictograph
   */
  async updateArrow(_pictographId, _arrowData) {
    throw new Error("updateArrow not yet implemented");
  }
  /**
   * Create a fallback SVG when rendering fails
   */
  createFallbackSVG() {
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("width", "300");
    svg.setAttribute("height", "300");
    svg.setAttribute("viewBox", "0 0 300 300");
    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("x", "10");
    rect.setAttribute("y", "10");
    rect.setAttribute("width", "280");
    rect.setAttribute("height", "280");
    rect.setAttribute("fill", "#f3f4f6");
    rect.setAttribute("stroke", "#e5e7eb");
    rect.setAttribute("stroke-width", "2");
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", "150");
    text.setAttribute("y", "150");
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("fill", "#6b7280");
    text.textContent = "Render Error";
    svg.appendChild(rect);
    svg.appendChild(text);
    return svg;
  }
}
class DefaultPropPositioner {
  constructor(gridData, gridMode) {
    this.gridData = gridData;
    this.gridMode = gridMode;
    if (!gridData || !gridData.allHandPointsNormal) {
      throw new Error("Invalid grid data provided to DefaultPropPositioner");
    }
    if (this.debugMode) {
      console.log(
        "🎯 DefaultPropPositioner initialized with grid mode:",
        gridMode
      );
    }
  }
  debugMode = false;
  fallbackCoordinates = {
    // Default positions if grid points aren't found - matching legacy fallbacks
    n: { x: 475, y: 330 },
    e: { x: 620, y: 475 },
    s: { x: 475, y: 620 },
    w: { x: 330, y: 475 },
    ne: { x: 620, y: 330 },
    se: { x: 620, y: 620 },
    sw: { x: 330, y: 620 },
    nw: { x: 330, y: 330 }
  };
  /**
   * Calculate coordinates for a prop based on its location
   */
  calculateCoordinates(location) {
    const pointName = `${location}_${this.gridMode}_hand_point`;
    const gridPoint = this.getGridPoint(pointName);
    if (gridPoint && gridPoint.coordinates) {
      if (this.debugMode) {
        console.log(
          `✅ Found grid point "${pointName}":`,
          gridPoint.coordinates
        );
      }
      return gridPoint.coordinates;
    } else {
      const fallback = this.getFallbackCoordinates(location);
      if (this.debugMode) {
        console.warn(
          `⚠️ Grid point "${pointName}" not found, using fallback: (${fallback.x}, ${fallback.y})`
        );
      }
      return fallback;
    }
  }
  /**
   * Get grid point by name from grid data
   */
  getGridPoint(pointName) {
    if (this.gridData.allHandPointsNormal && this.gridData.allHandPointsNormal[pointName]) {
      const point = this.gridData.allHandPointsNormal[pointName];
      if (point.coordinates) {
        return { coordinates: point.coordinates };
      }
    }
    const alternativeNames = [
      pointName,
      pointName.replace("_hand_point", ""),
      `${pointName}_normal`,
      `hand_${pointName}`
    ];
    for (const altName of alternativeNames) {
      if (this.gridData.allHandPointsNormal && this.gridData.allHandPointsNormal[altName]) {
        const point = this.gridData.allHandPointsNormal[altName];
        if (point.coordinates) {
          return { coordinates: point.coordinates };
        }
      }
    }
    return null;
  }
  /**
   * Get fallback coordinates for a location
   */
  getFallbackCoordinates(location) {
    return this.fallbackCoordinates[location] || { x: 475, y: 475 };
  }
  /**
   * Static helper method for quick coordinate calculation
   */
  static calculatePosition(location, gridMode = "diamond") {
    try {
      const gridData = createGridData(gridMode);
      const positioner = new DefaultPropPositioner(gridData, gridMode);
      return positioner.calculateCoordinates(location);
    } catch (error) {
      console.error("Error calculating position:", error);
      return { x: 475, y: 475 };
    }
  }
}
class PropRotAngleManager {
  loc;
  ori;
  constructor({ loc, ori }) {
    this.loc = loc;
    this.ori = ori;
  }
  /**
   * Get rotation angle based on location and orientation
   * Uses diamond vs box grid mode detection and appropriate angle maps
   */
  getRotationAngle() {
    const isDiamondLocation = ["n", "e", "s", "w"].includes(this.loc);
    const diamondAngleMap = {
      [Orientation.IN]: { n: 90, s: 270, w: 0, e: 180 },
      [Orientation.OUT]: { n: 270, s: 90, w: 180, e: 0 },
      [Orientation.CLOCK]: { n: 0, s: 180, w: 270, e: 90 },
      [Orientation.COUNTER]: { n: 180, s: 0, w: 90, e: 270 }
    };
    const boxAngleMap = {
      [Orientation.IN]: { ne: 135, nw: 45, sw: 315, se: 225 },
      [Orientation.OUT]: { ne: 315, nw: 225, sw: 135, se: 45 },
      [Orientation.CLOCK]: { ne: 45, nw: 315, sw: 225, se: 135 },
      [Orientation.COUNTER]: { ne: 225, nw: 135, sw: 45, se: 315 }
    };
    const angleMap = isDiamondLocation ? diamondAngleMap : boxAngleMap;
    const orientationAngles = angleMap[this.ori];
    return orientationAngles?.[this.loc] ?? 0;
  }
  /**
   * Static helper method for quick rotation calculation
   */
  static calculateRotation(loc, ori) {
    const manager = new PropRotAngleManager({ loc, ori });
    return manager.getRotationAngle();
  }
}
class PropRenderingService {
  svgCache = /* @__PURE__ */ new Map();
  SUPPORTED_PROPS = ["staff", "hand", "fan"];
  // Color transformation constants (matching desktop)
  COLOR_TRANSFORMATIONS = {
    blue: "#2E3192",
    red: "#ED1C24"
  };
  constructor() {
  }
  /**
   * Render a prop as an SVG element
   * DISABLED: Props are now rendered by Prop.svelte components to avoid duplicates
   */
  async renderProp(_propType, _color, _motionData, _gridMode = GridMode.DIAMOND) {
    const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
    group.setAttribute("class", "prop-service-disabled");
    return group;
  }
  /**
   * Calculate prop position based on motion data using real grid coordinates
   */
  async calculatePropPosition(motionData, color, gridMode = GridMode.DIAMOND) {
    try {
      const location = motionData?.end_loc || "s";
      const basePosition = DefaultPropPositioner.calculatePosition(
        location,
        gridMode
      );
      const rotation = this.calculatePropRotation(motionData, location);
      const offset = this.getColorOffset(color);
      return {
        x: basePosition.x + offset.x,
        y: basePosition.y + offset.y,
        rotation
      };
    } catch (error) {
      console.error("❌ Error calculating prop position:", error);
      return { x: 475, y: 475, rotation: 0 };
    }
  }
  /**
   * Load prop SVG with color transformation
   */
  async loadPropSVG(propType, color) {
    const cacheKey = `${propType}_${color}`;
    if (this.svgCache.has(cacheKey)) {
      const cached = this.svgCache.get(cacheKey);
      if (cached) return cached;
    }
    try {
      const response = await fetch(`/images/props/${propType}.svg`);
      if (!response.ok) {
        throw new Error(`Failed to load ${propType}.svg: ${response.status}`);
      }
      let svgContent = await response.text();
      svgContent = this.applyColorTransformation(svgContent, color);
      this.svgCache.set(cacheKey, svgContent);
      return svgContent;
    } catch (error) {
      console.error(`❌ Error loading ${propType} SVG:`, error);
      return this.createFallbackSVG(propType, color);
    }
  }
  /**
   * Get supported prop types
   */
  getSupportedPropTypes() {
    return [...this.SUPPORTED_PROPS];
  }
  /**
   * Apply color transformation to SVG content
   */
  applyColorTransformation(svgContent, color) {
    const targetColor = this.COLOR_TRANSFORMATIONS[color];
    svgContent = svgContent.replace(/fill="[^"]*"/g, `fill="${targetColor}"`);
    svgContent = svgContent.replace(/fill:[^;]*/g, `fill:${targetColor}`);
    svgContent = svgContent.replace(
      /stroke="[^"]*"/g,
      `stroke="${targetColor}"`
    );
    svgContent = svgContent.replace(/stroke:[^;]*/g, `stroke:${targetColor}`);
    return svgContent;
  }
  /**
   * Get coordinates for a location on the grid using real grid data
   */
  // getLocationCoordinates removed (unused)
  /**
   * Calculate prop rotation based on motion data using PropRotAngleManager for parity
   */
  calculatePropRotation(motionData, location) {
    const endLocation = location || motionData?.end_loc || "s";
    const endOrientation = motionData?.end_ori || "in";
    let orientation;
    switch (endOrientation) {
      case "in":
        orientation = Orientation.IN;
        break;
      case "out":
        orientation = Orientation.OUT;
        break;
      case "clock":
        orientation = Orientation.CLOCK;
        break;
      case "counter":
        orientation = Orientation.COUNTER;
        break;
      default:
        orientation = Orientation.IN;
    }
    return PropRotAngleManager.calculateRotation(endLocation, orientation);
  }
  getColorOffset(color) {
    return color === "blue" ? { x: -8, y: -8 } : { x: 8, y: 8 };
  }
  /**
   * Create fallback SVG for missing props
   */
  createFallbackSVG(propType, color) {
    const fillColor = this.COLOR_TRANSFORMATIONS[color];
    return `
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
				<rect x="10" y="10" width="80" height="80" fill="${fillColor}" opacity="0.5"/>
				<text x="50" y="55" text-anchor="middle" font-size="12" fill="white">${propType}</text>
			</svg>
		`;
  }
}
class SequenceDomainService {
  /**
   * Validate sequence creation request - REAL validation from desktop
   */
  validateCreateRequest(request) {
    const errors = [];
    if (!request.name || request.name.trim().length === 0) {
      errors.push({
        code: "MISSING_NAME",
        message: "Sequence name is required",
        field: "name",
        severity: "error"
      });
    }
    if (request.name && request.name.length > 100) {
      errors.push({
        code: "NAME_TOO_LONG",
        message: "Sequence name must be less than 100 characters",
        field: "name",
        severity: "error"
      });
    }
    if (request.length !== void 0 && (request.length < 0 || request.length > 64)) {
      errors.push({
        code: "INVALID_LENGTH",
        message: "Sequence length must be between 0 and 64",
        field: "length",
        severity: "error"
      });
    }
    if (request.gridMode && !["diamond", "box"].includes(request.gridMode)) {
      errors.push({
        code: "INVALID_GRID_MODE",
        message: 'Grid mode must be either "diamond" or "box"',
        field: "gridMode",
        severity: "error"
      });
    }
    return {
      isValid: errors.length === 0,
      errors,
      warnings: []
    };
  }
  /**
   * Create sequence with proper beat numbering - from desktop SequenceData
   */
  createSequence(request) {
    const validation = this.validateCreateRequest(request);
    if (!validation.isValid) {
      throw new Error(
        `Invalid sequence request: ${validation.errors.join(", ")}`
      );
    }
    const beats = [];
    for (let i = 1; i <= request.length; i++) {
      beats.push(this.createEmptyBeat(i));
    }
    const sequence = {
      id: this.generateId(),
      name: request.name.trim(),
      word: "",
      beats,
      thumbnails: [],
      is_favorite: false,
      is_circular: false,
      tags: [],
      metadata: { length: request.length }
    };
    return sequence;
  }
  /**
   * Update beat with proper validation - from desktop BeatSequenceService
   */
  updateBeat(sequence, beatIndex, beatData) {
    if (beatIndex < 0 || beatIndex >= sequence.beats.length) {
      throw new Error(`Invalid beat index: ${beatIndex}`);
    }
    if (beatData.duration && beatData.duration < 0) {
      throw new Error("Beat duration must be positive");
    }
    if (typeof beatData.beatNumber === "number") {
      if (beatData.beatNumber < 0) {
        throw new Error("Beat number must be non-negative");
      }
    }
    const newBeats = [...sequence.beats];
    newBeats[beatIndex] = { ...beatData };
    return { ...sequence, beats: newBeats };
  }
  /**
   * Calculate sequence word - from desktop SequenceWordCalculator
   */
  calculateSequenceWord(sequence) {
    if (!sequence.beats || sequence.beats.length === 0) {
      return "";
    }
    const word = sequence.beats.map(
      (beat) => beat.pictograph_data?.letter || beat.metadata?.letter || "?"
    ).join("");
    return this.simplifyRepeatedWord(word);
  }
  /**
   * Simplify repeated patterns - from desktop WordSimplifier
   */
  simplifyRepeatedWord(word) {
    if (!word) return word;
    const canFormByRepeating = (s, pattern) => {
      const patternLen = pattern.length;
      for (let i = 0; i < s.length; i += patternLen) {
        if (s.slice(i, i + patternLen) !== pattern) {
          return false;
        }
      }
      return true;
    };
    const n = word.length;
    for (let i = 1; i <= Math.floor(n / 2); i++) {
      const pattern = word.slice(0, i);
      if (n % i === 0 && canFormByRepeating(word, pattern)) {
        return pattern;
      }
    }
    return word;
  }
  /**
   * Create empty beat - from desktop BeatData structure
   */
  createEmptyBeat(beatNumber) {
    return {
      id: crypto.randomUUID(),
      beat_number: beatNumber,
      duration: 1,
      blue_reversal: false,
      red_reversal: false,
      is_blank: true,
      pictograph_data: null,
      metadata: {}
    };
  }
  /**
   * Generate unique ID - following desktop pattern
   */
  generateId() {
    return `seq_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
class SequenceGenerationService {
  constructor(motionGenerationService) {
    this.motionGenerationService = motionGenerationService;
  }
  /**
   * Generate a complete sequence
   */
  async generateSequence(options) {
    try {
      console.log("Generating sequence with options:", options);
      this.validateGenerationOptions(options);
      const beats = [];
      for (let i = 1; i <= options.length; i++) {
        const beat = await this.generateBeat(i, options, beats);
        beats.push(beat);
      }
      const generatedSequence = createSequenceData({
        name: this.generateSequenceName(options),
        word: "",
        // Will be calculated from beats
        beats,
        grid_mode: options.gridMode,
        prop_type: options.propType,
        difficulty_level: options.difficulty,
        is_favorite: false,
        is_circular: false,
        tags: [],
        metadata: {
          generated: true,
          generatedAt: (/* @__PURE__ */ new Date()).toISOString(),
          options
        }
      });
      console.log("Sequence generation complete:", generatedSequence.id);
      return generatedSequence;
    } catch (error) {
      console.error("Failed to generate sequence:", error);
      throw new Error(
        `Sequence generation failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Generate a single beat
   */
  async generateBeat(beatNumber, options, previousBeats) {
    try {
      console.log(`Generating beat ${beatNumber}/${options.length}`);
      const blueMotion = await this.motionGenerationService.generateMotion(
        "blue",
        options,
        previousBeats
      );
      const redMotion = await this.motionGenerationService.generateMotion(
        "red",
        options,
        previousBeats
      );
      const beat = {
        id: crypto.randomUUID(),
        beat_number: beatNumber,
        duration: 1,
        blue_reversal: false,
        red_reversal: false,
        is_blank: false,
        pictograph_data: null,
        // Will be set later with motions
        metadata: {
          generated: true,
          generatedAt: (/* @__PURE__ */ new Date()).toISOString(),
          difficulty: options.difficulty,
          letter: null,
          // Will be calculated later
          blueMotion,
          redMotion
        }
      };
      return beat;
    } catch (error) {
      console.error(`Failed to generate beat ${beatNumber}:`, error);
      throw new Error(
        `Beat generation failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Validate generation options
   */
  validateGenerationOptions(options) {
    if (!options.length || options.length < 1 || options.length > 64) {
      throw new Error("Sequence length must be between 1 and 64");
    }
    if (!Object.values(GridMode).includes(
      options.gridMode
    )) {
      throw new Error('Grid mode must be either "diamond" or "box"');
    }
    if (!["beginner", "intermediate", "advanced"].includes(options.difficulty)) {
      throw new Error(
        'Difficulty must be "beginner", "intermediate", or "advanced"'
      );
    }
  }
  /**
   * Generate a sequence name based on options
   */
  generateSequenceName(options) {
    const timestamp = (/* @__PURE__ */ new Date()).toLocaleString("en-US", {
      month: "short",
      day: "numeric",
      hour: "numeric",
      minute: "2-digit"
    });
    const difficulty = options.difficulty.charAt(0).toUpperCase() + options.difficulty.slice(1);
    return `${difficulty} ${options.length}-Beat (${timestamp})`;
  }
  /**
   * Generate sequence with specific patterns
   */
  async generatePatternSequence(pattern, options) {
    console.log(`Generating ${pattern} pattern sequence`);
    return this.generateSequence(options);
  }
  /**
   * Generate sequence variations
   */
  async generateVariations(baseSequence, variationType, count = 3) {
    console.log(`Generating ${count} ${variationType} variations`);
    const variations = [];
    for (let i = 0; i < count; i++) {
      const options = {
        length: baseSequence.beats.length || 8,
        gridMode: baseSequence.grid_mode || GridMode.DIAMOND,
        propType: baseSequence.prop_type || "fan",
        difficulty: baseSequence.difficulty_level || "intermediate"
      };
      const variation = await this.generateSequence(options);
      const namedVariation = createSequenceData({
        ...variation,
        name: `${baseSequence.name} - Variation ${i + 1}`
      });
      variations.push(namedVariation);
    }
    return variations;
  }
  /**
   * Get generation statistics
   */
  getGenerationStats() {
    return {
      totalGenerated: 0,
      averageGenerationTime: 0,
      lastGenerated: null
    };
  }
}
class SequenceService {
  constructor(sequenceDomainService, persistenceService) {
    this.sequenceDomainService = sequenceDomainService;
    this.persistenceService = persistenceService;
  }
  /**
   * Create a new sequence
   */
  async createSequence(request) {
    try {
      const sequence = this.sequenceDomainService.createSequence(request);
      await this.persistenceService.saveSequence(sequence);
      return sequence;
    } catch (error) {
      console.error("Failed to create sequence:", error);
      throw new Error(
        `Failed to create sequence: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Update a beat in a sequence
   */
  async updateBeat(sequenceId, beatIndex, beatData) {
    try {
      const currentSequence = await this.persistenceService.loadSequence(sequenceId);
      if (!currentSequence) {
        throw new Error(`Sequence ${sequenceId} not found`);
      }
      const updatedSequence = this.sequenceDomainService.updateBeat(
        currentSequence,
        beatIndex,
        beatData
      );
      await this.persistenceService.saveSequence(updatedSequence);
    } catch (error) {
      console.error("Failed to update beat:", error);
      throw new Error(
        `Failed to update beat: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Set the start position for a sequence
   */
  async setSequenceStartPosition(sequenceId, startPosition) {
    try {
      const currentSequence = await this.persistenceService.loadSequence(sequenceId);
      if (!currentSequence) {
        throw new Error(`Sequence ${sequenceId} not found`);
      }
      const updatedSequence = {
        ...currentSequence,
        start_position: startPosition
      };
      await this.persistenceService.saveSequence(updatedSequence);
    } catch (error) {
      console.error("Failed to set start position:", error);
      throw new Error(
        `Failed to set start position: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Delete a sequence
   */
  async deleteSequence(id) {
    try {
      await this.persistenceService.deleteSequence(id);
    } catch (error) {
      console.error("Failed to delete sequence:", error);
      throw new Error(
        `Failed to delete sequence: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Get a sequence by ID
   */
  async getSequence(id) {
    try {
      let sequence = await this.persistenceService.loadSequence(id);
      if (!sequence) {
        console.log(
          `🎬 Sequence ${id} not found, attempting to load from PNG metadata`
        );
        try {
          sequence = await this.loadSequenceFromPNG(id);
          if (sequence) {
            await this.persistenceService.saveSequence(sequence);
          }
        } catch (error) {
          console.error(`Failed to load sequence ${id} from PNG:`, error);
          return null;
        }
      }
      return sequence;
    } catch (error) {
      console.error(`Failed to get sequence ${id}:`, error);
      return null;
    }
  }
  /**
   * Get all sequences
   */
  async getAllSequences() {
    try {
      return await this.persistenceService.loadAllSequences();
    } catch (error) {
      console.error("Failed to get all sequences:", error);
      return [];
    }
  }
  /**
   * Add a beat to a sequence
   */
  async addBeat(sequenceId, beatData) {
    try {
      const sequence = await this.getSequence(sequenceId);
      if (!sequence) {
        throw new Error(`Sequence ${sequenceId} not found`);
      }
      const nextBeatNumber = sequence.beats.length + 1;
      const newBeat = {
        id: crypto.randomUUID(),
        beat_number: nextBeatNumber,
        duration: 1,
        blue_reversal: false,
        red_reversal: false,
        is_blank: true,
        pictograph_data: null,
        metadata: {},
        ...beatData
      };
      const updatedSequence = {
        ...sequence,
        beats: [...sequence.beats, newBeat]
      };
      await this.persistenceService.saveSequence(updatedSequence);
    } catch (error) {
      console.error("Failed to add beat:", error);
      throw new Error(
        `Failed to add beat: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Remove a beat from a sequence
   */
  async removeBeat(sequenceId, beatIndex) {
    try {
      const sequence = await this.getSequence(sequenceId);
      if (!sequence) {
        throw new Error(`Sequence ${sequenceId} not found`);
      }
      if (beatIndex < 0 || beatIndex >= sequence.beats.length) {
        throw new Error(`Beat index ${beatIndex} is out of range`);
      }
      const newBeats = sequence.beats.filter((_, index) => index !== beatIndex).map((beat, index) => ({ ...beat, beat_number: index + 1 }));
      const updatedSequence = { ...sequence, beats: newBeats };
      await this.persistenceService.saveSequence(updatedSequence);
    } catch (error) {
      console.error("Failed to remove beat:", error);
      throw new Error(
        `Failed to remove beat: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Load sequence from PNG metadata using the reliable PNG metadata extractor
   */
  async loadSequenceFromPNG(id) {
    console.log(`🎬 Loading sequence from PNG metadata for ID: ${id}`);
    try {
      const pngMetadata = await PngMetadataExtractor.extractSequenceMetadata(
        id.toUpperCase()
      );
      if (!pngMetadata || pngMetadata.length === 0) {
        console.error(`No metadata found in PNG for sequence: ${id}`);
        return null;
      }
      const sequence = await this.convertPngMetadataToSequence(id, pngMetadata);
      console.log(`✅ Loaded real sequence data from PNG for ${id}`);
      return sequence;
    } catch (error) {
      console.error(`Failed to load PNG metadata for ${id}:`, error);
      return this.createTestSequence(id);
    }
  }
  /**
   * Convert PNG metadata to SequenceData format
   */
  async convertPngMetadataToSequence(id, pngMetadata) {
    console.log(`🔄 Converting standalone data to web app format for ${id}`);
    const meta = pngMetadata[0];
    const steps = pngMetadata.slice(1);
    const beats = steps.filter((step) => step.beat && step.beat > 0).map((step) => ({
      id: `${step.beat}-${step.letter}`,
      beat_number: step.beat,
      duration: 1,
      blue_reversal: false,
      red_reversal: false,
      is_blank: false,
      pictograph_data: {
        id: `pictograph-${step.beat}`,
        grid_data: {
          grid_mode: meta.grid_mode || "diamond",
          center_x: 0,
          center_y: 0,
          radius: 100,
          grid_points: {}
        },
        arrows: {},
        props: {},
        motions: {
          blue: {
            motion_type: step.blue_attributes?.motion_type || "static",
            start_loc: step.blue_attributes?.start_loc || "s",
            end_loc: step.blue_attributes?.end_loc || "s",
            start_ori: step.blue_attributes?.start_ori || "in",
            end_ori: step.blue_attributes?.end_ori,
            // Don't set default - let it be undefined
            prop_rot_dir: step.blue_attributes?.prop_rot_dir || "no_rot",
            turns: step.blue_attributes?.turns || 0,
            is_visible: true
          },
          red: {
            motion_type: step.red_attributes?.motion_type || "static",
            start_loc: step.red_attributes?.start_loc || "s",
            end_loc: step.red_attributes?.end_loc || "s",
            start_ori: step.red_attributes?.start_ori || "in",
            end_ori: step.red_attributes?.end_ori,
            // Don't set default - let it be undefined
            prop_rot_dir: step.red_attributes?.prop_rot_dir || "no_rot",
            turns: step.red_attributes?.turns || 0,
            is_visible: true
          }
        },
        letter: step.letter || "",
        beat: step.beat,
        is_blank: false,
        is_mirrored: false,
        metadata: {}
      },
      metadata: {}
    }));
    console.log(`✅ Converted to web app format: ${beats.length} beats`);
    return {
      id,
      name: meta.word || id.toUpperCase(),
      word: meta.word || id.toUpperCase(),
      beats,
      thumbnails: [`${id.toUpperCase()}_ver1.png`],
      sequence_length: beats.length,
      author: meta.author || "Unknown",
      level: meta.level || 1,
      date_added: new Date(meta.date_added || Date.now()),
      grid_mode: meta.grid_mode || "diamond",
      prop_type: meta.prop_type || "unknown",
      is_favorite: meta.is_favorite || false,
      is_circular: meta.is_circular || false,
      starting_position: meta.sequence_start_position || "beta",
      difficulty_level: this.mapLevelToDifficulty(meta.level || 1),
      tags: ["flow", "practice"],
      metadata: {
        source: "png_metadata",
        extracted_at: (/* @__PURE__ */ new Date()).toISOString(),
        ...meta
      }
    };
  }
  /**
   * Map numeric level to difficulty string
   */
  mapLevelToDifficulty(level) {
    if (level <= 1) return "beginner";
    if (level <= 2) return "intermediate";
    return "advanced";
  }
  /**
   * Load sequence from PNG metadata or create fallback
   */
  async createTestSequence(id) {
    console.log(`🎬 Loading sequence from PNG metadata for ID: ${id}`);
    try {
      const sequenceData = await this.loadSequenceFromPNG(id);
      if (sequenceData) {
        console.log(`✅ Loaded real sequence data from PNG for ${id}`);
        return sequenceData;
      }
    } catch (error) {
      console.warn(`⚠️ Failed to load PNG metadata for ${id}:`, error);
    }
    throw new Error(
      `No PNG metadata found for sequence ${id}. Please ensure the sequence has a valid PNG thumbnail with embedded metadata.`
    );
  }
}
class SettingsService {
  SETTINGS_KEY = "tka-v2-settings";
  _settings = {
    theme: "dark",
    gridMode: GridMode.DIAMOND,
    showBeatNumbers: true,
    autoSave: true,
    exportQuality: "high",
    workbenchColumns: 3
  };
  constructor() {
    this.loadSettings();
  }
  /**
   * Get current settings
   */
  get currentSettings() {
    return { ...this._settings };
  }
  /**
   * Update a specific setting
   */
  async updateSetting(key, value) {
    try {
      this._settings[key] = value;
      await this.persistSettings();
      console.log(`Setting ${key} updated to:`, value);
    } catch (error) {
      console.error(`Failed to update setting ${key}:`, error);
      throw new Error(
        `Failed to update setting: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Load settings from storage
   */
  async loadSettings() {
    try {
      const stored = localStorage.getItem(this.SETTINGS_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        this._settings = { ...this._settings, ...parsed };
        console.log("Settings loaded:", this._settings);
      }
    } catch (error) {
      console.error("Failed to load settings:", error);
    }
  }
  /**
   * Persist settings to storage
   */
  async persistSettings() {
    try {
      localStorage.setItem(this.SETTINGS_KEY, JSON.stringify(this._settings));
    } catch (error) {
      console.error("Failed to persist settings:", error);
      throw error;
    }
  }
  /**
   * Reset settings to defaults
   */
  async resetToDefaults() {
    this._settings = {
      theme: "dark",
      gridMode: GridMode.DIAMOND,
      showBeatNumbers: true,
      autoSave: true,
      exportQuality: "high",
      workbenchColumns: 3
    };
    await this.persistSettings();
    console.log("Settings reset to defaults");
  }
}
class StartPositionService {
  DEFAULT_START_POSITIONS = {
    diamond: ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"],
    box: ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"]
  };
  constructor() {
    console.log("🎯 StartPositionService initialized");
  }
  async getAvailableStartPositions(propType, gridMode) {
    console.log(
      `📍 Getting available start positions for ${propType} in ${gridMode} mode`
    );
    try {
      const startPositionKeys = this.DEFAULT_START_POSITIONS[gridMode];
      const beatData = startPositionKeys.map((key, index) => {
        return createBeatData({
          beat_number: 0,
          is_blank: false,
          pictograph_data: this.createStartPositionPictograph(
            key,
            index,
            gridMode
          )
        });
      });
      console.log(`✅ Generated ${beatData.length} start positions`);
      return beatData;
    } catch (error) {
      console.error("❌ Error getting start positions:", error);
      return [];
    }
  }
  async setStartPosition(startPosition) {
    console.log(
      "🎯 Setting start position:",
      startPosition.pictograph_data?.id
    );
    try {
      if (typeof window !== "undefined") {
        const existingData = localStorage.getItem("start_position");
        if (existingData) {
          try {
            const parsed = JSON.parse(existingData);
            if (parsed.endPos) {
              console.log(
                "✅ Start position already in correct format, not overwriting"
              );
              return;
            }
          } catch {
          }
        }
        const optionPickerFormat = {
          endPos: startPosition.metadata?.endPos || "alpha1",
          // Extract from metadata
          pictograph_data: startPosition.pictograph_data,
          letter: startPosition.pictograph_data?.letter,
          gridMode: "diamond",
          // Default
          isStartPosition: true,
          // Include the full beat data for compatibility
          ...startPosition
        };
        localStorage.setItem(
          "start_position",
          JSON.stringify(optionPickerFormat)
        );
      }
      console.log("✅ Start position set successfully");
    } catch (error) {
      console.error("❌ Error setting start position:", error);
      throw new Error(
        `Failed to set start position: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  validateStartPosition(position) {
    const errors = [];
    if (!position.pictograph_data) {
      errors.push({
        code: "MISSING_PICTOGRAPH_DATA",
        message: "Start position must have pictograph data",
        severity: "error"
      });
    }
    if (!position.pictograph_data?.motions?.blue && !position.pictograph_data?.motions?.red) {
      errors.push({
        code: "MISSING_MOTIONS",
        message: "Start position must have at least one motion",
        severity: "error"
      });
    }
    if (position.pictograph_data?.motions?.blue?.motion_type !== MotionType.STATIC) {
      errors.push({
        code: "INVALID_BLUE_MOTION",
        message: "Blue motion must be static for start positions",
        severity: "error"
      });
    }
    if (position.pictograph_data?.motions?.red?.motion_type !== MotionType.STATIC) {
      errors.push({
        code: "INVALID_RED_MOTION",
        message: "Red motion must be static for start positions",
        severity: "error"
      });
    }
    return {
      isValid: errors.length === 0,
      errors,
      warnings: []
    };
  }
  async getDefaultStartPositions(gridMode) {
    console.log(`📍 Getting default start positions for ${gridMode} mode`);
    try {
      const startPositionKeys = this.DEFAULT_START_POSITIONS[gridMode];
      const pictographData = startPositionKeys.map(
        (key, index) => this.createStartPositionPictograph(key, index, gridMode)
      );
      console.log(
        `✅ Generated ${pictographData.length} default start positions`
      );
      return pictographData;
    } catch (error) {
      console.error("❌ Error getting default start positions:", error);
      return [];
    }
  }
  createStartPositionPictograph(key, index, gridMode) {
    let letter;
    if (key.includes("alpha")) letter = "α";
    else if (key.includes("beta")) letter = "β";
    else if (key.includes("gamma")) letter = "γ";
    else letter = key;
    const positionMappings = {
      alpha1_alpha1: { blue: Location.SOUTH, red: Location.NORTH },
      // Alpha1: Blue=South, Red=North
      beta5_beta5: { blue: Location.SOUTH, red: Location.SOUTH },
      // Beta5: Blue=South, Red=South
      gamma11_gamma11: { blue: Location.SOUTH, red: Location.EAST },
      // Gamma11: Blue=South, Red=East
      // Box mode positions
      alpha2_alpha2: { blue: Location.SOUTHWEST, red: Location.NORTHEAST },
      // Alpha2: Blue=Southwest, Red=Northeast
      beta4_beta4: { blue: Location.SOUTHEAST, red: Location.SOUTHEAST },
      // Beta4: Blue=Southeast, Red=Southeast
      gamma12_gamma12: { blue: Location.NORTHWEST, red: Location.NORTHEAST }
      // Gamma12: Blue=Northwest, Red=Northeast
    };
    const mapping = positionMappings[key];
    if (!mapping) {
      console.warn(`⚠️ No position mapping found for ${key}, using fallback`);
    }
    const blueLocation = mapping?.blue || Location.SOUTH;
    const redLocation = mapping?.red || Location.NORTH;
    console.log(
      `🎯 Creating start position ${key} - Blue: ${blueLocation}, Red: ${redLocation}`
    );
    const blueArrow = createArrowData({
      arrow_type: ArrowType.BLUE,
      color: "blue",
      turns: 0,
      location: blueLocation
    });
    const redArrow = createArrowData({
      arrow_type: ArrowType.RED,
      color: "red",
      turns: 0,
      location: redLocation
    });
    const blueProp = createPropData({
      prop_type: PropType.STAFF,
      color: "blue",
      location: blueLocation
    });
    const redProp = createPropData({
      prop_type: PropType.STAFF,
      color: "red",
      location: redLocation
    });
    const blueMotion = createMotionData({
      motion_type: MotionType.STATIC,
      prop_rot_dir: RotationDirection.NO_ROTATION,
      start_loc: blueLocation,
      end_loc: blueLocation,
      turns: 0,
      start_ori: Orientation.IN,
      end_ori: Orientation.IN
    });
    const redMotion = createMotionData({
      motion_type: MotionType.STATIC,
      prop_rot_dir: RotationDirection.NO_ROTATION,
      start_loc: redLocation,
      end_loc: redLocation,
      turns: 0,
      start_ori: Orientation.IN,
      end_ori: Orientation.IN
    });
    const pictograph = createPictographData({
      id: `start-pos-${key}-${index}`,
      grid_data: createGridData$1({
        grid_mode: gridMode === "diamond" ? GridMode.DIAMOND : GridMode.BOX
      }),
      arrows: { blue: blueArrow, red: redArrow },
      props: { blue: blueProp, red: redProp },
      motions: { blue: blueMotion, red: redMotion },
      letter,
      beat: index,
      is_blank: false,
      is_mirrored: false
    });
    return pictograph;
  }
}
const ISequenceServiceInterface = createServiceInterface$1(
  "ISequenceService",
  class extends SequenceService {
    constructor(...args) {
      super(
        args[0],
        args[1]
      );
    }
  }
);
const ISequenceDomainServiceInterface = createServiceInterface$1(
  "ISequenceDomainService",
  SequenceDomainService
);
const IPictographServiceInterface = createServiceInterface$1(
  "IPictographService",
  class extends PictographService {
    constructor(...args) {
      super(args[0]);
    }
  }
);
const IPictographRenderingServiceInterface = createServiceInterface$1(
  "IPictographRenderingService",
  class extends PictographRenderingService {
    constructor(...args) {
      super(
        args[0],
        args[1]
      );
    }
  }
);
const IPropRenderingServiceInterface = createServiceInterface$1(
  "IPropRenderingService",
  PropRenderingService
);
const IPersistenceServiceInterface = createServiceInterface$1(
  "IPersistenceService",
  LocalStoragePersistenceService
);
const ISettingsServiceInterface = createServiceInterface$1("ISettingsService", SettingsService);
const IDeviceDetectionServiceInterface = createServiceInterface$1(
  "IDeviceDetectionService",
  DeviceDetectionService
);
const IPanelManagementServiceInterface = createServiceInterface$1(
  "IPanelManagementService",
  PanelManagementService
);
const IApplicationInitializationServiceInterface = createServiceInterface$1(
  "IApplicationInitializationService",
  class extends ApplicationInitializationService {
    constructor(...args) {
      super(args[0], args[1]);
    }
  }
);
const IExportServiceInterface = createServiceInterface$1(
  "IExportService",
  class extends ExportService {
    constructor(...args) {
      super(args[0]);
    }
  }
);
const IMotionGenerationServiceInterface = createServiceInterface$1(
  "IMotionGenerationService",
  MotionGenerationService
);
const ISequenceGenerationServiceInterface = createServiceInterface$1(
  "ISequenceGenerationService",
  class extends SequenceGenerationService {
    constructor(...args) {
      super(args[0]);
    }
  }
);
const IConstructTabCoordinationServiceInterface = createServiceInterface$1(
  "IConstructTabCoordinationService",
  class extends ConstructTabCoordinationService {
    constructor(...args) {
      super(args[0], args[1]);
    }
  }
);
const IOptionDataServiceInterface = createServiceInterface$1(
  "IOptionDataService",
  OptionDataService
);
const IStartPositionServiceInterface = createServiceInterface$1(
  "IStartPositionService",
  StartPositionService
);
class ArrowPlacementDataService {
  allPlacements = {
    [GridMode.DIAMOND]: {},
    [GridMode.BOX]: {}
  };
  isDataLoaded = false;
  // File mapping for placement data
  placementFiles = {
    [GridMode.DIAMOND]: {
      pro: "/data/arrow_placement/diamond/default/default_diamond_pro_placements.json",
      anti: "/data/arrow_placement/diamond/default/default_diamond_anti_placements.json",
      float: "/data/arrow_placement/diamond/default/default_diamond_float_placements.json",
      dash: "/data/arrow_placement/diamond/default/default_diamond_dash_placements.json",
      static: "/data/arrow_placement/diamond/default/default_diamond_static_placements.json"
    },
    [GridMode.BOX]: {
      pro: "/data/arrow_placement/box/default/default_box_pro_placements.json",
      anti: "/data/arrow_placement/box/default/default_box_anti_placements.json",
      float: "/data/arrow_placement/box/default/default_box_float_placements.json",
      dash: "/data/arrow_placement/box/default/default_box_dash_placements.json",
      static: "/data/arrow_placement/box/default/default_box_static_placements.json"
    }
  };
  /**
   * Load all placement data from JSON files
   */
  async loadPlacementData() {
    if (this.isDataLoaded) {
      return;
    }
    console.log("Loading arrow placement data...");
    try {
      await this.loadGridPlacements(GridMode.DIAMOND);
      await this.loadGridPlacements(GridMode.BOX);
      this.isDataLoaded = true;
      console.log("✅ Arrow placement data loaded successfully");
    } catch (error) {
      console.error("❌ Failed to load arrow placement data:", error);
      throw new Error(
        `Placement data loading failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Load placements for a specific grid mode
   */
  async loadGridPlacements(gridMode) {
    const files = this.placementFiles[gridMode];
    this.allPlacements[gridMode] = {};
    for (const [motionType, filePath] of Object.entries(files)) {
      try {
        const placementData = await this.loadJsonFile(filePath);
        this.allPlacements[gridMode][motionType] = placementData;
        console.log(`Loaded ${motionType} placements for ${gridMode} grid`);
      } catch (error) {
        console.warn(
          `Could not load ${motionType} placements for ${gridMode}: ${error}`
        );
        this.allPlacements[gridMode][motionType] = {};
      }
    }
  }
  /**
   * Load JSON file with error handling
   */
  async loadJsonFile(path) {
    try {
      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.warn(`Failed to load placement data from ${path}:`, error);
      return {};
    }
  }
  /**
   * Get default adjustment using placement key and turns
   */
  async getDefaultAdjustment(motionType, placementKey, turns, gridMode = GridMode.DIAMOND) {
    await this.ensureDataLoaded();
    const gridPlacements = this.allPlacements[gridMode];
    if (!gridPlacements) {
      console.warn(`No placement data for grid mode: ${gridMode}`);
      return { x: 0, y: 0 };
    }
    const motionPlacements = gridPlacements[motionType];
    if (!motionPlacements) {
      console.warn(`No placement data for motion type: ${motionType}`);
      return { x: 0, y: 0 };
    }
    const placementData = motionPlacements[placementKey];
    if (!placementData) {
      console.warn(`No placement data for key: ${placementKey}`);
      return { x: 0, y: 0 };
    }
    const turnsStr = this.formatTurnsForLookup(turns);
    const adjustment = placementData[turnsStr];
    if (!adjustment) {
      console.warn(
        `No adjustment for turns: ${turnsStr} in placement: ${placementKey}`
      );
      return { x: 0, y: 0 };
    }
    const [x, y] = adjustment;
    console.log(
      `Found adjustment for ${motionType} ${placementKey} ${turnsStr}: [${x}, ${y}]`
    );
    return { x, y };
  }
  /**
   * Get available placement keys for a motion type
   */
  async getAvailablePlacementKeys(motionType, gridMode = GridMode.DIAMOND) {
    await this.ensureDataLoaded();
    const motionPlacements = this.allPlacements[gridMode]?.[motionType];
    if (!motionPlacements) {
      return [];
    }
    return Object.keys(motionPlacements);
  }
  /**
   * Check if data is loaded
   */
  isLoaded() {
    return this.isDataLoaded;
  }
  /**
   * Ensure data is loaded before operations
   */
  async ensureDataLoaded() {
    if (!this.isDataLoaded) {
      await this.loadPlacementData();
    }
  }
  /**
   * Format turns value for JSON lookup
   * Converts: 1.0 → "1", 0.5 → "0.5", etc.
   */
  formatTurnsForLookup(turns) {
    if (typeof turns === "string") {
      return turns;
    }
    if (turns === Math.floor(turns)) {
      return Math.floor(turns).toString();
    }
    return turns.toString();
  }
  /**
   * Debug method to log available keys
   */
  async debugAvailableKeys(motionType, gridMode = GridMode.DIAMOND) {
    const keys = await this.getAvailablePlacementKeys(motionType, gridMode);
    console.log(
      `Available placement keys for ${motionType} (${gridMode}):`,
      keys
    );
  }
  /**
   * Get raw placement data for debugging
   */
  async getPlacementData(motionType, placementKey, gridMode = GridMode.DIAMOND) {
    await this.ensureDataLoaded();
    const motionPlacements = this.allPlacements[gridMode]?.[motionType];
    return motionPlacements?.[placementKey] || {};
  }
}
class ArrowPlacementKeyService {
  // Letter condition mappings from desktop
  dashLetterConditions = {
    TYPE3: ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"],
    TYPE5: ["Φ-", "Ψ-", "Λ-"]
  };
  /**
   * Generate placement key based on motion data and pictograph context
   */
  getRawMotionType(motionData) {
    if ("motion_type" in motionData)
      return motionData.motion_type;
    return motionData.motionType;
  }
  generatePlacementKey(motionData, pictographData, availableKeys) {
    const rawMotionType = this.getRawMotionType(motionData);
    const motionType = this.normalizeMotionType(rawMotionType);
    const letter = pictographData.letter;
    console.log(
      `Generating placement key for ${motionType}, letter: ${letter}`
    );
    const candidateKeys = this.generateCandidateKeys(
      motionData,
      pictographData
    );
    for (const key of candidateKeys) {
      if (availableKeys.includes(key)) {
        console.log(`Selected placement key: ${key}`);
        return key;
      }
    }
    const fallback = motionType;
    console.log(`No specific key found, using fallback: ${fallback}`);
    return fallback;
  }
  /**
   * Generate basic key for motion type (fallback)
   */
  generateBasicKey(motionType) {
    return motionType;
  }
  /**
   * Generate candidate keys in order of preference
   */
  generateCandidateKeys(motionData, pictographData) {
    const rawMotionType = this.getRawMotionType(motionData);
    const motionType = this.normalizeMotionType(rawMotionType);
    const letter = pictographData.letter;
    const candidates = [];
    if (letter) {
      const letterSuffix = this.getLetterSuffix(letter);
      candidates.push(`${motionType}_to_layer1_alpha${letterSuffix}`);
      candidates.push(`${motionType}_to_layer2_alpha${letterSuffix}`);
      candidates.push(`${motionType}_to_layer1_beta${letterSuffix}`);
      candidates.push(`${motionType}_to_layer2_beta${letterSuffix}`);
      candidates.push(`${motionType}_to_layer1_gamma${letterSuffix}`);
      candidates.push(`${motionType}_to_layer2_gamma${letterSuffix}`);
      candidates.push(`${motionType}_to_radial_layer3_alpha${letterSuffix}`);
      candidates.push(`${motionType}_to_radial_layer3_beta${letterSuffix}`);
      candidates.push(`${motionType}_to_radial_layer3_gamma${letterSuffix}`);
      candidates.push(`${motionType}_to_nonradial_layer3_alpha${letterSuffix}`);
      candidates.push(`${motionType}_to_nonradial_layer3_beta${letterSuffix}`);
      candidates.push(`${motionType}_to_nonradial_layer3_gamma${letterSuffix}`);
    }
    candidates.push(`${motionType}_to_layer1_alpha`);
    candidates.push(`${motionType}_to_layer2_alpha`);
    candidates.push(`${motionType}_to_layer1_beta`);
    candidates.push(`${motionType}_to_layer2_beta`);
    candidates.push(`${motionType}_to_layer1_gamma`);
    candidates.push(`${motionType}_to_layer2_gamma`);
    candidates.push(`${motionType}_to_radial_layer3_alpha`);
    candidates.push(`${motionType}_to_radial_layer3_beta`);
    candidates.push(`${motionType}_to_radial_layer3_gamma`);
    candidates.push(`${motionType}_to_nonradial_layer3_alpha`);
    candidates.push(`${motionType}_to_nonradial_layer3_beta`);
    candidates.push(`${motionType}_to_nonradial_layer3_gamma`);
    candidates.push(motionType);
    return candidates;
  }
  /**
   * Get letter suffix for placement key
   */
  getLetterSuffix(letter) {
    if (!letter) {
      return "";
    }
    const allDashLetters = [
      ...this.dashLetterConditions.TYPE3,
      ...this.dashLetterConditions.TYPE5
    ];
    if (allDashLetters.includes(letter)) {
      const baseString = letter.slice(0, -1);
      return `_${baseString}_dash`;
    }
    return `_${letter}`;
  }
  /**
   * Normalize motion type to standard format
   */
  normalizeMotionType(motionType) {
    if (typeof motionType === "string") {
      const normalized = motionType.toLowerCase();
      if (["pro", "anti", "float", "dash", "static"].includes(normalized)) {
        return normalized;
      }
    }
    console.warn(
      `Invalid motion type: ${String(motionType)}, defaulting to 'pro'`
    );
    return "pro";
  }
  /**
   * Debug method to show all candidate keys
   */
  debugCandidateKeys(motionData, pictographData) {
    const candidates = this.generateCandidateKeys(motionData, pictographData);
    console.log("Candidate placement keys:", candidates);
    return candidates;
  }
}
let ArrowPositioningService$1 = class ArrowPositioningService {
  constructor(placementDataService, placementKeyService) {
    this.placementDataService = placementDataService;
    this.placementKeyService = placementKeyService;
  }
  CENTER_X = 475;
  CENTER_Y = 475;
  async calculateArrowPosition(_arrowData, _pictographData, _gridData) {
    try {
      return {
        x: this.CENTER_X,
        y: this.CENTER_Y,
        rotation: 0
      };
    } catch (error) {
      console.warn("Arrow positioning failed, using default position:", error);
      return {
        x: this.CENTER_X,
        y: this.CENTER_Y,
        rotation: 0
      };
    }
  }
  async calculateAllArrowPositions(pictographData, gridData) {
    const positions = /* @__PURE__ */ new Map();
    try {
      if (pictographData.arrows) {
        for (const [arrowId, arrowData] of Object.entries(
          pictographData.arrows
        )) {
          const position = await this.calculateArrowPosition(
            arrowData,
            pictographData,
            gridData
          );
          positions.set(arrowId, position);
        }
      }
    } catch (error) {
      console.warn("Failed to calculate all arrow positions:", error);
    }
    return positions;
  }
  calculateRotationAngle(_motion, _location, isMirrored) {
    try {
      let baseRotation = 0;
      if (isMirrored) {
        baseRotation = 180 - baseRotation;
      }
      return baseRotation;
    } catch (error) {
      console.warn("Rotation calculation failed, using default:", error);
      return 0;
    }
  }
  shouldMirrorArrow(motion) {
    try {
      return motion.prop_rot_dir === RotationDirection.COUNTER_CLOCKWISE;
    } catch (error) {
      console.warn("Mirror calculation failed, using default:", error);
      return false;
    }
  }
  /**
   * Get initial position based on location and grid data
   * @private - Reserved for future implementation
   */
  _getInitialPosition(location, gridData) {
    try {
      const gridPoint = gridData.allHandPointsNormal[location] || gridData.allLayer2PointsNormal[location];
      if (gridPoint && gridPoint.coordinates) {
        return {
          x: gridPoint.coordinates.x,
          y: gridPoint.coordinates.y
        };
      }
    } catch (error) {
      console.warn("Failed to get initial position from grid data:", error);
    }
    return { x: this.CENTER_X, y: this.CENTER_Y };
  }
  /**
   * Apply positioning adjustments based on motion and placement data
   * @private - Reserved for future implementation
   */
  async _applyPositionAdjustments(basePosition, _arrowData, _pictographData) {
    try {
      if (this.placementDataService && this.placementKeyService) {
      }
      return basePosition;
    } catch (error) {
      console.warn("Failed to apply position adjustments:", error);
      return basePosition;
    }
  }
};
class AttributeKeyGenerator {
  /**
   * Modern implementation of attribute key generation for arrow positioning.
   *
   * Generates keys used for special placement and default placement lookups.
   * Works with modern ArrowData and PictographData objects.
   */
  getKeyFromArrow(arrowData, pictographData) {
    try {
      const motionData = pictographData.motions?.[arrowData.color];
      if (!motionData) {
        console.debug(
          `No motion data for ${arrowData.color}, using color as key`
        );
        return arrowData.color;
      }
      const motionType = motionData.motion_type || "";
      const letter = pictographData.letter || "";
      const startOri = motionData.start_ori || "";
      const color = arrowData.color;
      const leadState = void 0;
      const hasHybridMotions = this.hasHybridMotions(pictographData);
      const startsFromMixedOrientation = this.startsFromMixedOrientation(pictographData);
      const startsFromStandardOrientation = !startsFromMixedOrientation;
      return this.generateKey(
        motionType,
        letter,
        startOri,
        color,
        leadState,
        hasHybridMotions,
        startsFromMixedOrientation,
        startsFromStandardOrientation
      );
    } catch (error) {
      console.error(
        `Error generating attribute key for ${arrowData.color}:`,
        error
      );
      return arrowData.color;
    }
  }
  generateKey(motionType, letter, startOri, color, leadState, hasHybridMotions, startsFromMixedOrientation, _startsFromStandardOrientation) {
    try {
      const IN = "in";
      const OUT = "out";
      const CLOCK = "clock";
      const COUNTER = "counter";
      if (startsFromMixedOrientation) {
        if (["S", "T"].includes(letter)) {
          return leadState || color;
        } else if (hasHybridMotions) {
          if ([IN, OUT].includes(startOri)) {
            return `${motionType}_from_layer1`;
          } else if ([CLOCK, COUNTER].includes(startOri)) {
            return `${motionType}_from_layer2`;
          } else {
            return color;
          }
        } else if (this.isNonHybridLetter(letter)) {
          return color;
        } else {
          return motionType;
        }
      } else {
        return color;
      }
    } catch (error) {
      console.error("Error in key generation:", error);
      return color;
    }
  }
  hasHybridMotions(pictographData) {
    try {
      const blueMotion = pictographData.motions?.blue;
      const redMotion = pictographData.motions?.red;
      if (!blueMotion || !redMotion) {
        return false;
      }
      const blueType = blueMotion.motion_type || "";
      const redType = redMotion.motion_type || "";
      return blueType !== redType;
    } catch {
      return false;
    }
  }
  startsFromMixedOrientation(pictographData) {
    try {
      const IN = "in";
      const OUT = "out";
      const blueMotion = pictographData.motions?.blue;
      const redMotion = pictographData.motions?.red;
      if (!blueMotion || !redMotion) {
        return false;
      }
      const blueStart = blueMotion.start_ori || "";
      const redStart = redMotion.start_ori || "";
      const blueLayer1 = [IN, OUT].includes(blueStart);
      const redLayer1 = [IN, OUT].includes(redStart);
      return blueLayer1 !== redLayer1;
    } catch {
      return false;
    }
  }
  isNonHybridLetter(letter) {
    const nonHybridLetters = [
      "A",
      "B",
      "D",
      "E",
      "G",
      "H",
      "J",
      "K",
      "M",
      "N",
      "P",
      "Q",
      "S",
      "T"
    ];
    return nonHybridLetters.includes(letter);
  }
}
class PlacementKeyGenerator {
  service = new ArrowPlacementKeyService();
  generatePlacementKey(motionData, pictographData, defaultPlacements, _gridMode) {
    const availableKeys = Object.keys(defaultPlacements || {});
    if (availableKeys.length === 0) {
      const candidates2 = this.service.debugCandidateKeys(
        motionData,
        pictographData
      );
      return candidates2[0] ?? this.service.generateBasicKey(
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        motionData.motion_type || "pro"
      );
    }
    const candidates = this.service.debugCandidateKeys(
      motionData,
      pictographData
    );
    for (const key of candidates) {
      if (availableKeys.includes(key)) return key;
    }
    return this.service.generateBasicKey(
      motionData.motion_type || "pro"
    );
  }
}
class SpecialPlacementOriKeyGenerator {
  generateOrientationKey(_motionData, pictographData) {
    try {
      const blueMotion = pictographData.motions?.blue;
      const redMotion = pictographData.motions?.red;
      if (blueMotion && redMotion) {
        const blueEndOri = blueMotion.end_ori || "in";
        const redEndOri = redMotion.end_ori || "in";
        const blueLayer = ["in", "out"].includes(blueEndOri) ? 1 : 2;
        const redLayer = ["in", "out"].includes(redEndOri) ? 1 : 2;
        if (blueLayer === 1 && redLayer === 1) return "from_layer1";
        if (blueLayer === 2 && redLayer === 2) return "from_layer2";
        if (blueLayer === 1 && redLayer === 2) return "from_layer3_blue1_red2";
        if (blueLayer === 2 && redLayer === 1) return "from_layer3_blue2_red1";
        return "from_layer1";
      }
    } catch {
    }
    return "from_layer1";
  }
}
class TurnsTupleKeyGenerator {
  generateTurnsTuple(pictographData) {
    try {
      const blueTurns = this.getTurns(pictographData.motions?.blue?.turns);
      const redTurns = this.getTurns(pictographData.motions?.red?.turns);
      return [blueTurns, redTurns];
    } catch {
      return [0, 0];
    }
  }
  getTurns(value) {
    if (typeof value === "number") return value;
    return 0;
  }
}
class ArrowAdjustmentLookup {
  /**
   * Focused service for arrow adjustment lookups.
   *
   * Handles the lookup phase of arrow positioning:
   * 1. Try special placement lookup (stored values)
   * 2. Fall back to default calculation
   * 3. Return proper Result types with error handling
   */
  specialPlacementService;
  defaultPlacementService;
  orientationKeyService;
  placementKeyService;
  turnsTupleService;
  attributeKeyService;
  constructor(specialPlacementService, defaultPlacementService, orientationKeyService, placementKeyService, turnsTupleService, attributeKeyService) {
    this.specialPlacementService = specialPlacementService;
    this.defaultPlacementService = defaultPlacementService;
    this.orientationKeyService = orientationKeyService;
    this.placementKeyService = placementKeyService;
    this.turnsTupleService = turnsTupleService;
    this.attributeKeyService = attributeKeyService;
  }
  async getBaseAdjustment(pictographData, motionData, letter, arrowColor) {
    if (!motionData || !letter) {
      throw new Error("Missing motion or letter data for adjustment lookup");
    }
    try {
      const [oriKey, turnsTuple, attrKey] = this.generateLookupKeys(
        pictographData,
        motionData
      );
      console.debug(
        `Generated keys - ori: ${oriKey}, turns: ${turnsTuple}, attr: ${attrKey}`
      );
      try {
        const specialAdjustment = await this.lookupSpecialPlacement(
          motionData,
          pictographData,
          arrowColor
        );
        return specialAdjustment;
      } catch {
        console.debug("No special placement found, falling back to default");
      }
      const defaultAdjustment = await this.calculateDefaultAdjustment(
        motionData,
        pictographData
      );
      console.debug(
        `Using default adjustment: (${defaultAdjustment.x.toFixed(1)}, ${defaultAdjustment.y.toFixed(1)})`
      );
      return defaultAdjustment;
    } catch (error) {
      console.error("Error in base adjustment lookup:", error);
      throw new Error(`Arrow adjustment lookup failed: ${error}`);
    }
  }
  generateLookupKeys(pictographData, motionData) {
    try {
      const oriKey = this.orientationKeyService.generateOrientationKey(
        motionData,
        pictographData
      );
      const turnsTuple = this.turnsTupleService.generateTurnsTuple(pictographData);
      const color = "blue";
      const tempArrow = {
        id: "temp",
        arrow_type: "BLUE",
        color,
        motion_type: motionData.motion_type || "",
        location: "center",
        start_orientation: motionData.start_ori || "",
        end_orientation: motionData.end_ori || "",
        rotation_direction: motionData.prop_rot_dir || "",
        turns: typeof motionData.turns === "number" ? motionData.turns : 0,
        is_mirrored: false,
        position_x: 0,
        position_y: 0,
        rotation_angle: 0,
        is_visible: true,
        is_selected: false
      };
      const attrKey = this.attributeKeyService.getKeyFromArrow(
        tempArrow,
        pictographData
      );
      return [oriKey, turnsTuple.join(","), attrKey];
    } catch (error) {
      console.error("Failed to generate lookup keys:", error);
      throw new Error(`Key generation failed: ${error}`);
    }
  }
  async lookupSpecialPlacement(motionData, pictographData, arrowColor) {
    try {
      const adjustment = await this.specialPlacementService.getSpecialAdjustment(
        motionData,
        pictographData,
        arrowColor
      );
      if (adjustment) {
        return adjustment;
      }
      throw new Error("No special placement found");
    } catch (error) {
      if (error instanceof Error && error.message === "No special placement found") {
        throw error;
      }
      console.error("Error in special placement lookup:", error);
      throw new Error(`Special placement lookup failed: ${error}`);
    }
  }
  async calculateDefaultAdjustment(motionData, pictographData, gridMode = "diamond") {
    try {
      const keys = await this.defaultPlacementService.getAvailablePlacementKeys(
        motionData.motion_type,
        pictographData.grid_mode
      );
      const defaultPlacements = Object.fromEntries(
        (keys || []).map((k) => [k, true])
      );
      const placementKey = this.placementKeyService.generatePlacementKey(
        motionData,
        pictographData,
        defaultPlacements,
        gridMode
      );
      const adjustmentPoint = await this.defaultPlacementService.getDefaultAdjustment(
        placementKey,
        motionData.turns || 0,
        motionData.motion_type,
        gridMode
      );
      return adjustmentPoint;
    } catch (error) {
      console.error("Error calculating default adjustment:", error);
      throw new Error(`Default adjustment calculation failed: ${error}`);
    }
  }
}
class DefaultPlacementService {
  placementDataService;
  constructor() {
    this.placementDataService = new ArrowPlacementDataService();
  }
  /**
   * Get default adjustment for arrow placement using placement key and turns.
   * This mirrors the Python get_default_adjustment() method.
   *
   * @param placementKey - The placement identifier
   * @param turns - Number of turns or turn identifier
   * @param motionType - Motion type (pro, anti, float, dash, static)
   * @param gridMode - Grid mode (diamond, box)
   * @returns Adjustment coordinates {x, y}
   */
  async getDefaultAdjustment(placementKey, turns, motionType, gridMode) {
    console.log(
      `DefaultPlacementService.getDefaultAdjustment() called with:`,
      `placement_key=${placementKey}, turns=${turns}, motion_type=${motionType}, grid_mode=${gridMode}`
    );
    try {
      await this._loadAllDefaultPlacements();
      const adjustment = await this.placementDataService.getDefaultAdjustment(
        motionType,
        placementKey,
        turns,
        gridMode
      );
      console.log(
        `Found default adjustment for ${placementKey} at ${turns} turns: [${adjustment.x}, ${adjustment.y}]`
      );
      return adjustment;
    } catch (error) {
      console.warn(
        `Failed to get default adjustment for ${placementKey} at ${turns} turns:`,
        error
      );
      return { x: 0, y: 0 };
    }
  }
  /**
   * Get available placement keys for a given motion type and grid mode.
   * This mirrors the Python get_available_placement_keys() method.
   *
   * @param motionType - Motion type (pro, anti, float, dash, static)
   * @param gridMode - Grid mode (diamond, box)
   * @returns Array of available placement key strings
   */
  async getAvailablePlacementKeys(motionType, gridMode) {
    await this._loadAllDefaultPlacements();
    return this.placementDataService.getAvailablePlacementKeys(
      motionType,
      gridMode
    );
  }
  /**
   * Check if placement data has been loaded.
   * This mirrors the Python is_loaded() method.
   *
   * @returns true if data is loaded, false otherwise
   */
  isLoaded() {
    return this.placementDataService.isLoaded();
  }
  /**
   * Load all default placement data from JSON files.
   * This mirrors the Python _load_all_default_placements() method.
   *
   * The Python version loads from:
   * - /data/arrow_placement/{grid_mode}/default/{motion_type}_placements.json
   *
   * Our TypeScript version uses the same file structure and loading pattern.
   */
  async _loadAllDefaultPlacements() {
    if (this.placementDataService.isLoaded()) {
      return;
    }
    console.log("DefaultPlacementService: Loading all default placements...");
    try {
      await this.placementDataService.loadPlacementData();
      console.log(
        "✅ DefaultPlacementService: All placement data loaded successfully"
      );
    } catch (error) {
      console.error(
        "❌ DefaultPlacementService: Failed to load placement data:",
        error
      );
      throw new Error(
        `Default placement loading failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
  /**
   * Get raw placement data for debugging purposes.
   * This mirrors the Python get_placement_data() method.
   *
   * @param motionType - Motion type (pro, anti, float, dash, static)
   * @param placementKey - The placement identifier
   * @param gridMode - Grid mode (diamond, box)
   * @returns Raw placement data mapping turns to [x, y] adjustments
   */
  async getPlacementData(motionType, placementKey, gridMode) {
    await this._loadAllDefaultPlacements();
    return this.placementDataService.getPlacementData(
      motionType,
      placementKey,
      gridMode
    );
  }
  /**
   * Debug method to log available placement keys.
   * This mirrors the Python debug_available_keys() method.
   *
   * @param motionType - Motion type to debug
   * @param gridMode - Grid mode to debug
   */
  async debugAvailableKeys(motionType, gridMode) {
    await this._loadAllDefaultPlacements();
    await this.placementDataService.debugAvailableKeys(motionType, gridMode);
  }
}
class SpecialPlacementService {
  // Structure: [gridMode][oriKey][letter] -> Record<string, unknown>
  specialPlacements = {};
  loadingCache = /* @__PURE__ */ new Set();
  constructor() {
    this.specialPlacements = { diamond: {}, box: {} };
  }
  /**
   * Get special adjustment for arrow based on special placement logic.
   *
   * @param motionData Motion data containing motion information
   * @param pictographData Pictograph data containing letter and context
   * @param arrowColor Color of the arrow ('red' or 'blue') - if not provided, will try to determine from motion
   * @returns Point with special adjustment or null if no special placement found
   */
  async getSpecialAdjustment(motionData, pictographData, arrowColor) {
    if (!motionData || !pictographData.letter) {
      return null;
    }
    const motion = motionData;
    const letter = pictographData.letter;
    const oriKey = this.generateOrientationKey(motion, pictographData);
    const gridMode = pictographData.grid_mode || "diamond";
    const turnsTuple = this.generateTurnsTuple(pictographData);
    await this.ensureLetterPlacementsLoaded(gridMode, oriKey, letter);
    const letterData = this.specialPlacements[gridMode]?.[oriKey]?.[letter];
    if (!letterData) {
      return null;
    }
    const turnData = letterData?.[turnsTuple];
    if (!turnData) {
      return null;
    }
    let colorKey = "";
    if (arrowColor) {
      colorKey = arrowColor;
    } else if (pictographData.motions?.blue && pictographData.motions.blue === motion) {
      colorKey = "blue";
    } else if (pictographData.motions?.red && pictographData.motions.red === motion) {
      colorKey = "red";
    } else {
      colorKey = "blue";
    }
    if (colorKey in turnData) {
      const adjustmentValues = turnData[colorKey];
      if (Array.isArray(adjustmentValues) && adjustmentValues.length === 2) {
        return { x: adjustmentValues[0], y: adjustmentValues[1] };
      }
    }
    const motionTypeKey = motionData.motion_type?.toLowerCase() || "";
    if (motionTypeKey in turnData) {
      const adjustmentValues = turnData[motionTypeKey];
      if (Array.isArray(adjustmentValues) && adjustmentValues.length === 2) {
        return { x: adjustmentValues[0], y: adjustmentValues[1] };
      }
    }
    return null;
  }
  /**
   * Load special placement data from JSON configuration files.
   */
  async ensureLetterPlacementsLoaded(gridMode, oriKey, letter) {
    try {
      if (!this.specialPlacements[gridMode]) {
        this.specialPlacements[gridMode] = {};
      }
      if (!this.specialPlacements[gridMode][oriKey]) {
        this.specialPlacements[gridMode][oriKey] = {};
      }
      if (this.specialPlacements[gridMode][oriKey][letter]) {
        return;
      }
      const cacheKey = `${gridMode}:${oriKey}:${letter}`;
      if (this.loadingCache.has(cacheKey)) {
        return;
      }
      this.loadingCache.add(cacheKey);
      const encodedLetter = encodeURIComponent(letter);
      const basePath = `/data/arrow_placement/${gridMode}/special/${oriKey}/${encodedLetter}_placements.json`;
      try {
        const response = await fetch(basePath);
        if (!response.ok) {
          console.debug(
            `No special placement file for ${gridMode}/${oriKey}/${letter}: ${response.status} ${response.statusText}`
          );
          this.specialPlacements[gridMode][oriKey][letter] = {};
          return;
        }
        const data = await response.json();
        this.specialPlacements[gridMode][oriKey][letter] = data;
        console.debug(
          `Loaded special placements for ${gridMode}/${oriKey}/${letter}`
        );
      } catch (error) {
        console.debug(
          `Failed to load special placements for ${gridMode}/${oriKey}/${letter} from ${basePath}:`,
          error
        );
        this.specialPlacements[gridMode][oriKey][letter] = {};
      }
    } catch (error) {
      console.error("Error ensuring special placement data:", error);
    }
  }
  /**
   * Generate orientation key matching the ori_key_generator logic.
   *
   * This determines which subfolder of special placements to use:
   * - from_layer1: Basic orientations
   * - from_layer2: Layer 2 orientations
   * - from_layer3_blue1_red2: Mixed orientations with blue on layer 1, red on layer 2
   * - from_layer3_blue2_red1: Mixed orientations with blue on layer 2, red on layer 1
   */
  generateOrientationKey(_motion, pictographData) {
    try {
      const blueMotion = pictographData.motions?.blue;
      const redMotion = pictographData.motions?.red;
      if (blueMotion && redMotion) {
        const blueEndOri = blueMotion.end_ori || "in";
        const redEndOri = redMotion.end_ori || "in";
        const blueLayer = ["in", "out"].includes(blueEndOri) ? 1 : 2;
        const redLayer = ["in", "out"].includes(redEndOri) ? 1 : 2;
        if (blueLayer === 1 && redLayer === 1) {
          return "from_layer1";
        }
        if (blueLayer === 2 && redLayer === 2) {
          return "from_layer2";
        }
        if (blueLayer === 1 && redLayer === 2) {
          return "from_layer3_blue1_red2";
        }
        if (blueLayer === 2 && redLayer === 1) {
          return "from_layer3_blue2_red1";
        }
        return "from_layer1";
      }
    } catch (error) {
      console.debug("Error generating orientation key:", error);
    }
    return "from_layer1";
  }
  /**
   * Generate turns tuple string matching the turns_tuple_generator logic.
   *
   * This creates a string representation of the turn values for lookup in JSON data.
   * Format: "(blue_turns, red_turns)" e.g., "(0, 1.5)", "(1, 0.5)"
   */
  generateTurnsTuple(pictographData) {
    try {
      const blueMotion = pictographData.motions?.blue;
      const redMotion = pictographData.motions?.red;
      if (blueMotion && redMotion) {
        const blueTurns = typeof blueMotion.turns === "number" ? blueMotion.turns : 0;
        const redTurns = typeof redMotion.turns === "number" ? redMotion.turns : 0;
        const blueStr = blueTurns === Math.floor(blueTurns) ? Math.floor(blueTurns).toString() : blueTurns.toString();
        const redStr = redTurns === Math.floor(redTurns) ? Math.floor(redTurns).toString() : redTurns.toString();
        return `(${blueStr}, ${redStr})`;
      }
      return "(0, 0)";
    } catch (error) {
      console.debug("Error generating turns tuple:", error);
      return "(0, 0)";
    }
  }
}
class DirectionalTupleCalculator {
  /**
   * Calculator for directional tuples used in arrow positioning.
   */
  calculateDirectionalTuple(_motion, _location) {
    return [0, 0];
  }
  generateDirectionalTuples(motion, baseX, baseY) {
    const mt = String(motion.motion_type).toLowerCase();
    const rot = String(motion.prop_rot_dir).toLowerCase();
    const NE = Location.NORTHEAST;
    const SE = Location.SOUTHEAST;
    const SW = Location.SOUTHWEST;
    const NW = Location.NORTHWEST;
    const N = Location.NORTH;
    const E = Location.EAST;
    const S = Location.SOUTH;
    const W = Location.WEST;
    const diagonalSet = /* @__PURE__ */ new Set([NE, SE, SW, NW]);
    const gridIsDiamond = diagonalSet.has(motion.start_loc) || diagonalSet.has(motion.end_loc);
    const isCW = rot === "clockwise" || rot === "cw";
    const isCCW = rot === "counter_clockwise" || rot === "ccw";
    const isNoRot = rot === "no_rot";
    const tuple = (a, b) => [a, b];
    const shiftDiamond = () => {
      if (mt === "float") {
        const order = [NE, SE, SW, NW];
        const idxStart = order.indexOf(motion.start_loc);
        const idxEnd = order.indexOf(motion.end_loc);
        const cwStep = (idxStart + 1) % 4 === idxEnd;
        if (cwStep) {
          return [
            tuple(baseX, baseY),
            tuple(-baseY, baseX),
            tuple(-baseX, -baseY),
            tuple(baseY, -baseX)
          ];
        } else {
          return [
            tuple(-baseY, -baseX),
            tuple(baseX, -baseY),
            tuple(baseY, baseX),
            tuple(-baseX, baseY)
          ];
        }
      }
      if (mt === "pro" && isCW)
        return [
          tuple(baseX, baseY),
          tuple(-baseY, baseX),
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX)
        ];
      if (mt === "pro" && isCCW)
        return [
          tuple(-baseY, -baseX),
          tuple(baseX, -baseY),
          tuple(baseY, baseX),
          tuple(-baseX, baseY)
        ];
      if (mt === "anti" && isCW)
        return [
          tuple(-baseY, -baseX),
          tuple(baseX, -baseY),
          tuple(baseY, baseX),
          tuple(-baseX, baseY)
        ];
      if (mt === "anti" && isCCW)
        return [
          tuple(baseX, baseY),
          tuple(-baseY, baseX),
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX)
        ];
      return [
        tuple(baseX, baseY),
        tuple(baseX, baseY),
        tuple(baseX, baseY),
        tuple(baseX, baseY)
      ];
    };
    const shiftBox = () => {
      if (mt === "float") {
        const order = [N, E, S, W];
        const idxStart = order.indexOf(motion.start_loc);
        const idxEnd = order.indexOf(motion.end_loc);
        const cwStep = (idxStart + 1) % 4 === idxEnd;
        if (cwStep) {
          return [
            tuple(baseX, baseY),
            tuple(-baseY, baseX),
            tuple(-baseX, -baseY),
            tuple(baseY, -baseX)
          ];
        } else {
          return [
            tuple(-baseY, -baseX),
            tuple(baseX, -baseY),
            tuple(baseY, baseX),
            tuple(-baseX, baseY)
          ];
        }
      }
      if (mt === "pro" && isCW)
        return [
          tuple(-baseX, baseY),
          tuple(-baseY, -baseX),
          tuple(baseX, -baseY),
          tuple(baseY, baseX)
        ];
      if (mt === "pro" && isCCW)
        return [
          tuple(baseX, baseY),
          tuple(-baseY, baseX),
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX)
        ];
      if (mt === "anti" && isCW)
        return [
          tuple(-baseX, baseY),
          tuple(-baseY, -baseX),
          tuple(baseX, -baseY),
          tuple(baseY, baseX)
        ];
      if (mt === "anti" && isCCW)
        return [
          tuple(baseX, baseY),
          tuple(-baseY, baseX),
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX)
        ];
      return [
        tuple(baseX, baseY),
        tuple(baseX, baseY),
        tuple(baseX, baseY),
        tuple(baseX, baseY)
      ];
    };
    const dashDiamond = () => {
      if (isCW)
        return [
          tuple(baseX, -baseY),
          tuple(baseY, baseX),
          tuple(-baseX, baseY),
          tuple(-baseY, -baseX)
        ];
      if (isCCW)
        return [
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX),
          tuple(baseX, baseY),
          tuple(-baseY, baseX)
        ];
      if (isNoRot)
        return [
          tuple(baseX, baseY),
          tuple(-baseY, -baseX),
          tuple(baseX, -baseY),
          tuple(baseY, baseX)
        ];
      return [
        tuple(baseX, baseY),
        tuple(baseX, baseY),
        tuple(baseX, baseY),
        tuple(baseX, baseY)
      ];
    };
    const dashBox = () => {
      if (isCW)
        return [
          tuple(-baseY, baseX),
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX),
          tuple(baseX, baseY)
        ];
      if (isCCW)
        return [
          tuple(-baseX, baseY),
          tuple(-baseY, -baseX),
          tuple(baseX, -baseY),
          tuple(baseY, baseX)
        ];
      if (isNoRot)
        return [
          tuple(baseX, baseY),
          tuple(-baseY, baseX),
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX)
        ];
      return [
        tuple(baseX, baseY),
        tuple(baseX, baseY),
        tuple(baseX, baseY),
        tuple(baseX, baseY)
      ];
    };
    const staticDiamond = () => {
      if (isCW)
        return [
          tuple(baseX, -baseY),
          tuple(baseY, baseX),
          tuple(-baseX, baseY),
          tuple(-baseY, -baseX)
        ];
      if (isCCW)
        return [
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX),
          tuple(baseX, baseY),
          tuple(-baseY, baseX)
        ];
      return [
        tuple(baseX, baseY),
        tuple(-baseX, -baseY),
        tuple(-baseY, baseX),
        tuple(baseY, -baseX)
      ];
    };
    const staticBox = () => {
      if (isCW)
        return [
          tuple(baseX, baseY),
          tuple(-baseY, baseX),
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX)
        ];
      if (isCCW)
        return [
          tuple(-baseY, -baseX),
          tuple(baseX, -baseY),
          tuple(baseY, baseX),
          tuple(-baseX, baseY)
        ];
      return [
        tuple(baseX, baseY),
        tuple(-baseY, baseX),
        tuple(-baseX, -baseY),
        tuple(baseY, -baseX)
      ];
    };
    if (mt === "dash") return gridIsDiamond ? dashDiamond() : dashBox();
    if (mt === "static") return gridIsDiamond ? staticDiamond() : staticBox();
    return gridIsDiamond ? shiftDiamond() : shiftBox();
  }
}
class QuadrantIndexCalculator {
  /**
   * Calculator for quadrant indices used in directional tuple selection.
   */
  calculateQuadrantIndex(location) {
    const quadrantMap = {
      [Location.NORTHEAST]: 0,
      [Location.SOUTHEAST]: 1,
      [Location.SOUTHWEST]: 2,
      [Location.NORTHWEST]: 3,
      // Cardinal directions map to nearest quadrant
      [Location.NORTH]: 0,
      // Maps to NE quadrant
      [Location.EAST]: 1,
      // Maps to SE quadrant
      [Location.SOUTH]: 2,
      // Maps to SW quadrant
      [Location.WEST]: 3
      // Maps to NW quadrant
    };
    return quadrantMap[location] || 0;
  }
}
class DirectionalTupleProcessor {
  /**
   * Processor for applying directional tuple adjustments to arrow positioning.
   */
  constructor(directionalTupleService, quadrantIndexService) {
    this.directionalTupleService = directionalTupleService;
    this.quadrantIndexService = quadrantIndexService;
  }
  processDirectionalTuples(baseAdjustment, _motion, location) {
    try {
      const directionalTuples = this.directionalTupleService.generateDirectionalTuples(
        _motion,
        baseAdjustment.x,
        baseAdjustment.y
      );
      const quadrantIndex = this.quadrantIndexService.calculateQuadrantIndex(location);
      const selectedTuple = directionalTuples[quadrantIndex] || [0, 0];
      return { x: selectedTuple[0], y: selectedTuple[1] };
    } catch (error) {
      console.warn(
        "Directional tuple processing failed, using base adjustment:",
        error
      );
      return baseAdjustment;
    }
  }
}
class ArrowAdjustmentCalculator {
  /**
   * Clean coordinator service for arrow positioning with proper error handling.
   *
   * Delegates to focused services:
   * - ArrowAdjustmentLookup: Special/default placement lookups
   * - DirectionalTupleProcessor: Tuple generation and selection
   *
   * Provides comprehensive arrow positioning adjustment calculation.
   */
  lookupService;
  tupleProcessor;
  constructor(lookupService, tupleProcessor) {
    this.lookupService = lookupService || this.createDefaultLookupService();
    this.tupleProcessor = tupleProcessor || this.createDefaultTupleProcessor();
  }
  async calculateAdjustment(pictographData, motionData, letter, location, arrowColor) {
    try {
      return await this.calculateAdjustmentResult(
        pictographData,
        motionData,
        letter,
        location,
        arrowColor
      );
    } catch (error) {
      console.error(`Adjustment calculation failed: ${error}`);
      return { x: 0, y: 0 };
    }
  }
  async calculateAdjustmentResult(pictographData, motionData, letter, location, arrowColor) {
    try {
      const baseAdjustment = await this.lookupService.getBaseAdjustment(
        pictographData,
        motionData,
        letter,
        arrowColor
      );
      const finalAdjustment = this.tupleProcessor.processDirectionalTuples(
        baseAdjustment,
        motionData,
        location
      );
      return finalAdjustment;
    } catch (error) {
      console.error(
        `Adjustment calculation failed for letter ${letter}: ${error}`
      );
      throw new Error(`Arrow adjustment calculation failed: ${error}`);
    }
  }
  calculateAdjustmentSync(pictographData, motionData, letter, location, arrowColor) {
    try {
      const baseAdjustment = this.getBasicAdjustmentSync(motionData);
      const finalAdjustment = this.tupleProcessor.processDirectionalTuples(
        baseAdjustment,
        motionData,
        location
      );
      console.debug(
        `Sync adjustment for ${motionData.motion_type} ${motionData.turns} turns at ${location}: (${finalAdjustment.x}, ${finalAdjustment.y})`
      );
      return finalAdjustment;
    } catch (error) {
      console.warn(
        `Sync adjustment calculation failed for letter ${letter}: ${error}`
      );
      return { x: 0, y: 0 };
    }
  }
  getBasicAdjustmentSync(motionData) {
    const motionType = motionData.motion_type;
    const turns = typeof motionData.turns === "number" ? motionData.turns : 0;
    const turnsStr = turns === Math.floor(turns) ? turns.toString() : turns.toString();
    const placementData = {
      [MotionType.PRO]: {
        "0": [-10, -40],
        "0.5": [30, 105],
        "1": [30, 25],
        "1.5": [-35, 145],
        "2": [-10, -35],
        "2.5": [20, 100],
        "3": [30, 25]
      },
      [MotionType.ANTI]: {
        "0": [0, -40],
        "0.5": [-15, 110],
        "1": [0, -40],
        "1.5": [20, 155],
        "2": [0, -40],
        "2.5": [0, 100],
        "3": [0, -50]
      },
      [MotionType.STATIC]: {
        "0": [0, 0],
        "0.5": [0, -140],
        "1": [50, 50],
        "1.5": [0, 0],
        "2": [0, 0],
        "2.5": [0, 0],
        "3": [0, 0]
      },
      [MotionType.DASH]: {
        "0": [0, 0]
      },
      [MotionType.FLOAT]: {
        fl: [30, -30]
      }
    };
    const motionAdjustments = placementData[motionType];
    if (motionAdjustments && motionAdjustments[turnsStr]) {
      const [x, y] = motionAdjustments[turnsStr];
      return { x, y };
    }
    return { x: 0, y: 0 };
  }
  createDefaultLookupService() {
    return new ArrowAdjustmentLookup(
      new SpecialPlacementService(),
      new DefaultPlacementService(),
      new SpecialPlacementOriKeyGenerator(),
      new PlacementKeyGenerator(),
      new TurnsTupleKeyGenerator(),
      new AttributeKeyGenerator()
    );
  }
  createDefaultTupleProcessor() {
    return new DirectionalTupleProcessor(
      new DirectionalTupleCalculator(),
      new QuadrantIndexCalculator()
    );
  }
}
class DashLocationCalculator {
  /**
   * Dash location calculation service.
   *
   * Implements comprehensive dash location calculation logic including:
   * - Φ_DASH and Ψ_DASH special handling
   * - Λ (Lambda) zero turns special case
   * - Type 3 scenario detection and handling
   * - Grid mode specific calculations (Diamond/Box)
   * - Complex location mappings for different scenarios
   */
  // Predefined location mappings for dash calculations - comprehensive mapping
  PHI_DASH_PSI_DASH_LOCATION_MAP = {
    [`red,${Location.NORTH},${Location.SOUTH}`]: Location.EAST,
    [`red,${Location.EAST},${Location.WEST}`]: Location.NORTH,
    [`red,${Location.SOUTH},${Location.NORTH}`]: Location.EAST,
    [`red,${Location.WEST},${Location.EAST}`]: Location.NORTH,
    [`blue,${Location.NORTH},${Location.SOUTH}`]: Location.WEST,
    [`blue,${Location.EAST},${Location.WEST}`]: Location.SOUTH,
    [`blue,${Location.SOUTH},${Location.NORTH}`]: Location.WEST,
    [`blue,${Location.WEST},${Location.EAST}`]: Location.SOUTH,
    [`red,${Location.NORTHWEST},${Location.SOUTHEAST}`]: Location.NORTHEAST,
    [`red,${Location.NORTHEAST},${Location.SOUTHWEST}`]: Location.SOUTHEAST,
    [`red,${Location.SOUTHWEST},${Location.NORTHEAST}`]: Location.SOUTHEAST,
    [`red,${Location.SOUTHEAST},${Location.NORTHWEST}`]: Location.NORTHEAST,
    [`blue,${Location.NORTHWEST},${Location.SOUTHEAST}`]: Location.SOUTHWEST,
    [`blue,${Location.NORTHEAST},${Location.SOUTHWEST}`]: Location.NORTHWEST,
    [`blue,${Location.SOUTHWEST},${Location.NORTHEAST}`]: Location.NORTHWEST,
    [`blue,${Location.SOUTHEAST},${Location.NORTHWEST}`]: Location.SOUTHWEST
  };
  LAMBDA_ZERO_TURNS_LOCATION_MAP = {
    [`${Location.NORTH},${Location.SOUTH},${Location.WEST}`]: Location.EAST,
    [`${Location.EAST},${Location.WEST},${Location.SOUTH}`]: Location.NORTH,
    [`${Location.NORTH},${Location.SOUTH},${Location.EAST}`]: Location.WEST,
    [`${Location.WEST},${Location.EAST},${Location.SOUTH}`]: Location.NORTH,
    [`${Location.SOUTH},${Location.NORTH},${Location.WEST}`]: Location.EAST,
    [`${Location.EAST},${Location.WEST},${Location.NORTH}`]: Location.SOUTH,
    [`${Location.SOUTH},${Location.NORTH},${Location.EAST}`]: Location.WEST,
    [`${Location.WEST},${Location.EAST},${Location.NORTH}`]: Location.SOUTH,
    [`${Location.NORTHEAST},${Location.SOUTHWEST},${Location.NORTHWEST}`]: Location.SOUTHEAST,
    [`${Location.NORTHWEST},${Location.SOUTHEAST},${Location.NORTHEAST}`]: Location.SOUTHWEST,
    [`${Location.SOUTHWEST},${Location.NORTHEAST},${Location.SOUTHEAST}`]: Location.NORTHWEST,
    [`${Location.SOUTHEAST},${Location.NORTHWEST},${Location.SOUTHWEST}`]: Location.NORTHEAST,
    [`${Location.NORTHEAST},${Location.SOUTHWEST},${Location.SOUTHEAST}`]: Location.NORTHWEST,
    [`${Location.NORTHWEST},${Location.SOUTHEAST},${Location.SOUTHWEST}`]: Location.NORTHEAST,
    [`${Location.SOUTHWEST},${Location.NORTHEAST},${Location.NORTHWEST}`]: Location.SOUTHEAST,
    [`${Location.SOUTHEAST},${Location.NORTHWEST},${Location.NORTHEAST}`]: Location.SOUTHWEST
  };
  LAMBDA_DASH_ZERO_TURNS_LOCATION_MAP = {
    [`${Location.NORTH},${Location.SOUTH},${Location.WEST}`]: Location.EAST,
    [`${Location.EAST},${Location.WEST},${Location.SOUTH}`]: Location.NORTH,
    [`${Location.NORTH},${Location.SOUTH},${Location.EAST}`]: Location.WEST,
    [`${Location.WEST},${Location.EAST},${Location.SOUTH}`]: Location.NORTH,
    [`${Location.SOUTH},${Location.NORTH},${Location.WEST}`]: Location.EAST,
    [`${Location.EAST},${Location.WEST},${Location.NORTH}`]: Location.SOUTH,
    [`${Location.SOUTH},${Location.NORTH},${Location.EAST}`]: Location.WEST,
    [`${Location.WEST},${Location.EAST},${Location.NORTH}`]: Location.SOUTH,
    [`${Location.NORTHEAST},${Location.SOUTHWEST},${Location.NORTHWEST}`]: Location.SOUTHEAST,
    [`${Location.NORTHWEST},${Location.SOUTHEAST},${Location.NORTHEAST}`]: Location.SOUTHWEST,
    [`${Location.SOUTHWEST},${Location.NORTHEAST},${Location.SOUTHEAST}`]: Location.NORTHWEST,
    [`${Location.SOUTHEAST},${Location.NORTHWEST},${Location.SOUTHWEST}`]: Location.NORTHEAST,
    [`${Location.NORTHEAST},${Location.SOUTHWEST},${Location.SOUTHEAST}`]: Location.NORTHWEST,
    [`${Location.NORTHWEST},${Location.SOUTHEAST},${Location.SOUTHWEST}`]: Location.NORTHEAST,
    [`${Location.SOUTHWEST},${Location.NORTHEAST},${Location.NORTHWEST}`]: Location.SOUTHEAST,
    [`${Location.SOUTHEAST},${Location.NORTHWEST},${Location.NORTHEAST}`]: Location.SOUTHWEST
  };
  DEFAULT_ZERO_TURNS_DASH_LOCATION_MAP = {
    [`${Location.NORTH},${Location.SOUTH}`]: Location.EAST,
    [`${Location.EAST},${Location.WEST}`]: Location.SOUTH,
    [`${Location.SOUTH},${Location.NORTH}`]: Location.WEST,
    [`${Location.WEST},${Location.EAST}`]: Location.NORTH,
    [`${Location.NORTHEAST},${Location.SOUTHWEST}`]: Location.SOUTHEAST,
    [`${Location.NORTHWEST},${Location.SOUTHEAST}`]: Location.NORTHEAST,
    [`${Location.SOUTHWEST},${Location.NORTHEAST}`]: Location.NORTHWEST,
    [`${Location.SOUTHEAST},${Location.NORTHWEST}`]: Location.SOUTHWEST
  };
  NON_ZERO_TURNS_DASH_LOCATION_MAP = {
    clockwise: {
      [Location.NORTH]: Location.EAST,
      [Location.EAST]: Location.SOUTH,
      [Location.SOUTH]: Location.WEST,
      [Location.WEST]: Location.NORTH,
      [Location.NORTHEAST]: Location.SOUTHEAST,
      [Location.SOUTHEAST]: Location.SOUTHWEST,
      [Location.SOUTHWEST]: Location.NORTHWEST,
      [Location.NORTHWEST]: Location.NORTHEAST
    },
    counter_clockwise: {
      [Location.NORTH]: Location.WEST,
      [Location.EAST]: Location.NORTH,
      [Location.SOUTH]: Location.EAST,
      [Location.WEST]: Location.SOUTH,
      [Location.NORTHEAST]: Location.NORTHWEST,
      [Location.SOUTHEAST]: Location.NORTHEAST,
      [Location.SOUTHWEST]: Location.SOUTHEAST,
      [Location.NORTHWEST]: Location.SOUTHWEST
    }
  };
  DIAMOND_DASH_LOCATION_MAP = {
    [`${Location.NORTH},${Location.NORTHWEST}`]: Location.EAST,
    [`${Location.NORTH},${Location.NORTHEAST}`]: Location.WEST,
    [`${Location.NORTH},${Location.SOUTHEAST}`]: Location.WEST,
    [`${Location.NORTH},${Location.SOUTHWEST}`]: Location.EAST,
    [`${Location.EAST},${Location.NORTHWEST}`]: Location.SOUTH,
    [`${Location.EAST},${Location.NORTHEAST}`]: Location.SOUTH,
    [`${Location.EAST},${Location.SOUTHEAST}`]: Location.NORTH,
    [`${Location.EAST},${Location.SOUTHWEST}`]: Location.NORTH,
    [`${Location.SOUTH},${Location.NORTHWEST}`]: Location.EAST,
    [`${Location.SOUTH},${Location.NORTHEAST}`]: Location.WEST,
    [`${Location.SOUTH},${Location.SOUTHEAST}`]: Location.WEST,
    [`${Location.SOUTH},${Location.SOUTHWEST}`]: Location.EAST,
    [`${Location.WEST},${Location.NORTHWEST}`]: Location.SOUTH,
    [`${Location.WEST},${Location.NORTHEAST}`]: Location.SOUTH,
    [`${Location.WEST},${Location.SOUTHEAST}`]: Location.NORTH,
    [`${Location.WEST},${Location.SOUTHWEST}`]: Location.NORTH
  };
  BOX_DASH_LOCATION_MAP = {
    [`${Location.NORTHEAST},${Location.NORTH}`]: Location.SOUTHEAST,
    [`${Location.NORTHEAST},${Location.EAST}`]: Location.NORTHWEST,
    [`${Location.NORTHEAST},${Location.SOUTH}`]: Location.NORTHWEST,
    [`${Location.NORTHEAST},${Location.WEST}`]: Location.SOUTHEAST,
    [`${Location.SOUTHEAST},${Location.NORTH}`]: Location.SOUTHWEST,
    [`${Location.SOUTHEAST},${Location.EAST}`]: Location.SOUTHWEST,
    [`${Location.SOUTHEAST},${Location.SOUTH}`]: Location.NORTHEAST,
    [`${Location.SOUTHEAST},${Location.WEST}`]: Location.NORTHEAST,
    [`${Location.SOUTHWEST},${Location.NORTH}`]: Location.SOUTHEAST,
    [`${Location.SOUTHWEST},${Location.EAST}`]: Location.NORTHWEST,
    [`${Location.SOUTHWEST},${Location.SOUTH}`]: Location.NORTHWEST,
    [`${Location.SOUTHWEST},${Location.WEST}`]: Location.SOUTHEAST,
    [`${Location.NORTHWEST},${Location.NORTH}`]: Location.SOUTHWEST,
    [`${Location.NORTHWEST},${Location.EAST}`]: Location.SOUTHWEST,
    [`${Location.NORTHWEST},${Location.SOUTH}`]: Location.NORTHEAST,
    [`${Location.NORTHWEST},${Location.WEST}`]: Location.NORTHEAST
  };
  calculateDashLocationFromPictographData(pictographData, isBlueArrow) {
    const motion = isBlueArrow ? pictographData.motions?.blue : pictographData.motions?.red;
    const otherMotion = isBlueArrow ? pictographData.motions?.red : pictographData.motions?.blue;
    if (!motion || motion.motion_type?.toLowerCase() !== "dash") {
      return motion?.start_loc || Location.NORTH;
    }
    const letterInfo = this.getLetterInfo(pictographData);
    const gridInfo = this.getGridInfo(pictographData);
    const arrowColor = this.getArrowColor(isBlueArrow);
    return this.calculateDashLocation(
      motion,
      otherMotion,
      letterInfo.letterType,
      arrowColor,
      gridInfo.gridMode,
      gridInfo.shiftLocation,
      letterInfo.isPhiDash,
      letterInfo.isPsiDash,
      letterInfo.isLambda,
      letterInfo.isLambdaDash
    );
  }
  calculateDashLocation(motion, otherMotion, letterType, arrowColor, gridMode, shiftLocation, isPhiDash = false, isPsiDash = false, isLambda = false, isLambdaDash = false) {
    if (isPhiDash || isPsiDash) {
      return this.getPhiDashPsiDashLocation(motion, otherMotion, arrowColor);
    }
    if (isLambda && motion.turns === 0 && otherMotion) {
      return this.getLambdaZeroTurnsLocation(motion, otherMotion);
    }
    if (isLambdaDash && motion.turns === 0 && otherMotion) {
      return this.getLambdaDashZeroTurnsLocation(motion, otherMotion);
    }
    if (motion.turns === 0) {
      return this.defaultZeroTurnsDashLocation(
        motion,
        letterType,
        gridMode,
        shiftLocation
      );
    }
    return this.dashLocationNonZeroTurns(motion);
  }
  getLambdaDashZeroTurnsLocation(motion, otherMotion) {
    const key = `${motion.start_loc},${motion.end_loc},${otherMotion.end_loc}`;
    return this.LAMBDA_DASH_ZERO_TURNS_LOCATION_MAP[key] || motion.start_loc;
  }
  getPhiDashPsiDashLocation(motion, otherMotion, arrowColor) {
    if (!otherMotion || !arrowColor) {
      return this.defaultZeroTurnsDashLocation(motion);
    }
    if (motion.turns === 0 && otherMotion.turns === 0) {
      const key = `${arrowColor},${motion.start_loc},${motion.end_loc}`;
      return this.PHI_DASH_PSI_DASH_LOCATION_MAP[key] || motion.start_loc;
    }
    if (motion.turns === 0) {
      const oppositeLocation = this.dashLocationNonZeroTurns(otherMotion);
      return this.getOppositeLocation(oppositeLocation);
    }
    return this.dashLocationNonZeroTurns(motion);
  }
  getLambdaZeroTurnsLocation(motion, otherMotion) {
    const key = `${motion.start_loc},${motion.end_loc},${otherMotion.end_loc}`;
    return this.LAMBDA_ZERO_TURNS_LOCATION_MAP[key] || motion.start_loc;
  }
  defaultZeroTurnsDashLocation(motion, letterType, gridMode, shiftLocation) {
    if (letterType === "Type3" && gridMode && shiftLocation) {
      return this.calculateDashLocationBasedOnShift(
        motion,
        gridMode,
        shiftLocation
      );
    }
    const key = `${motion.start_loc},${motion.end_loc}`;
    return this.DEFAULT_ZERO_TURNS_DASH_LOCATION_MAP[key] || motion.start_loc;
  }
  dashLocationNonZeroTurns(motion) {
    const rotDir = motion.prop_rot_dir?.toLowerCase();
    if (rotDir === "no_rotation" || rotDir === "none") {
      return motion.start_loc;
    }
    const directionMap = this.NON_ZERO_TURNS_DASH_LOCATION_MAP[rotDir] || this.NON_ZERO_TURNS_DASH_LOCATION_MAP["clockwise"];
    return directionMap?.[motion.start_loc] || motion.start_loc;
  }
  calculateDashLocationBasedOnShift(motion, gridMode, shiftLocation) {
    const startLoc = motion.start_loc;
    if (gridMode === "diamond") {
      const key = `${startLoc},${shiftLocation}`;
      return this.DIAMOND_DASH_LOCATION_MAP[key] || startLoc;
    } else if (gridMode === "box") {
      const key = `${startLoc},${shiftLocation}`;
      return this.BOX_DASH_LOCATION_MAP[key] || startLoc;
    }
    return this.defaultZeroTurnsDashLocation(motion);
  }
  getOppositeLocation(location) {
    const oppositeMap = {
      [Location.NORTH]: Location.SOUTH,
      [Location.SOUTH]: Location.NORTH,
      [Location.EAST]: Location.WEST,
      [Location.WEST]: Location.EAST,
      [Location.NORTHEAST]: Location.SOUTHWEST,
      [Location.SOUTHWEST]: Location.NORTHEAST,
      [Location.SOUTHEAST]: Location.NORTHWEST,
      [Location.NORTHWEST]: Location.SOUTHEAST
    };
    return oppositeMap[location] || location;
  }
  // Simplified helper methods for extracting information from pictograph data
  getLetterInfo(pictographData) {
    const letter = pictographData.letter?.toUpperCase() || "";
    return {
      letterType: "TYPE1",
      // Simplified - would need proper letter analysis
      isPhiDash: letter.includes("Φ_DASH") || letter.includes("PHI_DASH"),
      isPsiDash: letter.includes("Ψ_DASH") || letter.includes("PSI_DASH"),
      isLambda: letter.includes("Λ") || letter === "LAMBDA",
      isLambdaDash: letter.includes("Λ_DASH") || letter.includes("LAMBDA_DASH")
    };
  }
  getGridInfo(pictographData) {
    const result = {
      gridMode: pictographData.grid_mode || "diamond"
    };
    return result;
  }
  getArrowColor(isBlueArrow) {
    return isBlueArrow ? "blue" : "red";
  }
}
class ArrowLocationCalculator {
  /**
   * Pure algorithmic service for calculating arrow locations.
   *
   * Implements location calculation algorithms without any UI dependencies.
   * Each motion type has its own calculation strategy.
   */
  dashLocationService;
  // Direction pairs mapping for shift arrows (PRO/ANTI/FLOAT)
  // Maps start/end location pairs to their calculated arrow location
  shiftDirectionPairs = {
    // Cardinal + Diagonal combinations
    [this.createLocationPairKey([Location.NORTH, Location.EAST])]: Location.NORTHEAST,
    [this.createLocationPairKey([Location.EAST, Location.SOUTH])]: Location.SOUTHEAST,
    [this.createLocationPairKey([Location.SOUTH, Location.WEST])]: Location.SOUTHWEST,
    [this.createLocationPairKey([Location.WEST, Location.NORTH])]: Location.NORTHWEST,
    // Diagonal + Cardinal combinations
    [this.createLocationPairKey([Location.NORTHEAST, Location.NORTHWEST])]: Location.NORTH,
    [this.createLocationPairKey([Location.NORTHEAST, Location.SOUTHEAST])]: Location.EAST,
    [this.createLocationPairKey([Location.SOUTHWEST, Location.SOUTHEAST])]: Location.SOUTH,
    [this.createLocationPairKey([Location.NORTHWEST, Location.SOUTHWEST])]: Location.WEST
  };
  constructor(dashLocationService) {
    this.dashLocationService = dashLocationService || new DashLocationCalculator();
  }
  calculateLocation(motion, pictographData) {
    const motionType = motion.motion_type?.toLowerCase();
    switch (motionType) {
      case "static":
        return this.calculateStaticLocation(motion);
      case "pro":
      case "anti":
      case "float":
        return this.calculateShiftLocation(motion);
      case "dash":
        return this.calculateDashLocation(motion, pictographData);
      default:
        console.warn(
          `Unknown motion type: ${motionType}, using start location`
        );
        return motion.start_loc || Location.NORTH;
    }
  }
  calculateStaticLocation(motion) {
    return motion.start_loc || Location.NORTH;
  }
  calculateShiftLocation(motion) {
    if (!motion.start_loc || !motion.end_loc) {
      console.warn(
        "Shift motion missing start_loc or end_loc, using start_loc"
      );
      return motion.start_loc || Location.NORTH;
    }
    const locationPairKey = this.createLocationPairKey([
      motion.start_loc,
      motion.end_loc
    ]);
    const calculatedLocation = this.shiftDirectionPairs[locationPairKey] || motion.start_loc;
    return calculatedLocation;
  }
  calculateDashLocation(motion, pictographData) {
    if (!pictographData) {
      console.warn(
        "No pictograph data provided for dash location calculation, using start location"
      );
      return motion.start_loc || Location.NORTH;
    }
    const isBlueArrow = this.isBlueArrowMotion(motion, pictographData);
    return this.dashLocationService.calculateDashLocationFromPictographData(
      pictographData,
      isBlueArrow
    );
  }
  getSupportedMotionTypes() {
    return ["static", "pro", "anti", "float", "dash"];
  }
  validateMotionData(motion) {
    if (!motion) {
      return false;
    }
    const motionType = motion.motion_type?.toLowerCase();
    if (!this.getSupportedMotionTypes().includes(motionType)) {
      return false;
    }
    if (["pro", "anti", "float"].includes(motionType || "")) {
      return motion.start_loc != null && motion.end_loc != null;
    }
    if (["static", "dash"].includes(motionType || "")) {
      return motion.start_loc != null;
    }
    return true;
  }
  extractBeatDataFromPictograph(pictograph) {
    if (!pictograph.arrows) {
      return null;
    }
    const blueMotion = pictograph.motions?.blue;
    const redMotion = pictograph.motions?.red;
    return {
      beatNumber: pictograph.metadata?.created_from_beat || 1,
      letter: pictograph.letter,
      pictographData: {
        motions: {
          blue: blueMotion,
          red: redMotion
        }
      }
    };
  }
  isBlueArrowMotion(motion, pictographData) {
    if (pictographData.motions?.blue === motion) {
      return true;
    }
    if (pictographData.motions?.red === motion) {
      return false;
    }
    console.warn("Could not determine arrow color for motion, assuming blue");
    return true;
  }
  /**
   * Create a normalized key for location pairs to enable bidirectional lookup.
   * This ensures that [A, B] and [B, A] produce the same key.
   */
  createLocationPairKey(locations) {
    const sortedLocations = [...locations].sort();
    return sortedLocations.join(",");
  }
}
class ArrowRotationCalculator {
  /**
   * Pure algorithmic service for calculating arrow rotation angles.
   *
   * Implements rotation calculation algorithms without any UI dependencies.
   * Each motion type has its own rotation strategy based on proven algorithms.
   */
  // Static arrow rotation angles (arrows point inward by default)
  staticRotationMap = {
    [Location.NORTH]: 180,
    [Location.NORTHEAST]: 225,
    [Location.EAST]: 270,
    [Location.SOUTHEAST]: 315,
    [Location.SOUTH]: 0,
    [Location.SOUTHWEST]: 45,
    [Location.WEST]: 90,
    [Location.NORTHWEST]: 135
  };
  // PRO rotation angles by rotation direction
  proClockwiseMap = {
    [Location.NORTH]: 315,
    [Location.EAST]: 45,
    [Location.SOUTH]: 135,
    [Location.WEST]: 225,
    [Location.NORTHEAST]: 0,
    [Location.SOUTHEAST]: 90,
    [Location.SOUTHWEST]: 180,
    [Location.NORTHWEST]: 270
  };
  proCounterClockwiseMap = {
    [Location.NORTH]: 315,
    [Location.EAST]: 225,
    [Location.SOUTH]: 135,
    [Location.WEST]: 45,
    [Location.NORTHEAST]: 90,
    [Location.SOUTHEAST]: 180,
    [Location.SOUTHWEST]: 270,
    [Location.NORTHWEST]: 0
  };
  // ANTI rotation angles by rotation direction
  antiClockwiseMap = {
    [Location.NORTH]: 315,
    [Location.EAST]: 225,
    [Location.SOUTH]: 135,
    [Location.WEST]: 45,
    [Location.NORTHEAST]: 90,
    [Location.SOUTHEAST]: 180,
    [Location.SOUTHWEST]: 270,
    [Location.NORTHWEST]: 0
  };
  antiCounterClockwiseMap = {
    [Location.NORTH]: 315,
    [Location.EAST]: 45,
    [Location.SOUTH]: 135,
    [Location.WEST]: 225,
    [Location.NORTHEAST]: 0,
    [Location.SOUTHEAST]: 90,
    [Location.SOUTHWEST]: 180,
    [Location.NORTHWEST]: 270
  };
  // DASH rotation angles by rotation direction
  dashClockwiseMap = {
    [Location.NORTH]: 270,
    [Location.EAST]: 0,
    [Location.SOUTH]: 90,
    [Location.WEST]: 180,
    [Location.NORTHEAST]: 315,
    [Location.SOUTHEAST]: 45,
    [Location.SOUTHWEST]: 135,
    [Location.NORTHWEST]: 225
  };
  dashCounterClockwiseMap = {
    [Location.NORTH]: 270,
    [Location.EAST]: 180,
    [Location.SOUTH]: 90,
    [Location.WEST]: 0,
    [Location.NORTHEAST]: 225,
    [Location.SOUTHEAST]: 135,
    [Location.SOUTHWEST]: 45,
    [Location.NORTHWEST]: 315
  };
  // DASH NO_ROTATION mapping (start_loc, end_loc) -> angle
  dashNoRotationMap = {
    [`${Location.NORTH},${Location.SOUTH}`]: 90,
    [`${Location.EAST},${Location.WEST}`]: 180,
    [`${Location.SOUTH},${Location.NORTH}`]: 270,
    [`${Location.WEST},${Location.EAST}`]: 0,
    [`${Location.SOUTHEAST},${Location.NORTHWEST}`]: 225,
    [`${Location.SOUTHWEST},${Location.NORTHEAST}`]: 315,
    [`${Location.NORTHWEST},${Location.SOUTHEAST}`]: 45,
    [`${Location.NORTHEAST},${Location.SOUTHWEST}`]: 135
  };
  calculateRotation(motion, location) {
    const motionType = motion.motion_type?.toLowerCase();
    switch (motionType) {
      case "static":
        return this.calculateStaticRotation(location);
      case "pro":
        return this.calculateProRotation(motion, location);
      case "anti":
        return this.calculateAntiRotation(motion, location);
      case "dash":
        return this.calculateDashRotation(motion, location);
      case "float":
        return this.calculateFloatRotation(motion, location);
      default:
        console.warn(`Unknown motion type: ${motionType}, returning 0.0`);
        return 0;
    }
  }
  calculateStaticRotation(location) {
    return this.staticRotationMap[location] || 0;
  }
  calculateProRotation(motion, location) {
    const rotDir = motion.prop_rot_dir?.toLowerCase();
    if (rotDir === "clockwise" || rotDir === "cw") {
      return this.proClockwiseMap[location] || 0;
    } else {
      return this.proCounterClockwiseMap[location] || 0;
    }
  }
  calculateAntiRotation(motion, location) {
    const rotDir = motion.prop_rot_dir?.toLowerCase();
    if (rotDir === "clockwise" || rotDir === "cw") {
      return this.antiClockwiseMap[location] || 0;
    } else {
      return this.antiCounterClockwiseMap[location] || 0;
    }
  }
  calculateDashRotation(motion, location) {
    const rotDir = motion.prop_rot_dir?.toLowerCase();
    if (rotDir === "no_rotation" || rotDir === "none") {
      const key = `${motion.start_loc},${motion.end_loc}`;
      return this.dashNoRotationMap[key] || 0;
    }
    if (rotDir === "clockwise" || rotDir === "cw") {
      return this.dashClockwiseMap[location] || 0;
    } else {
      return this.dashCounterClockwiseMap[location] || 0;
    }
  }
  calculateFloatRotation(motion, location) {
    return this.calculateProRotation(motion, location);
  }
  getSupportedMotionTypes() {
    return ["static", "pro", "anti", "dash", "float"];
  }
  validateMotionData(motion) {
    if (!motion) {
      return false;
    }
    const motionType = motion.motion_type?.toLowerCase();
    if (!this.getSupportedMotionTypes().includes(motionType)) {
      return false;
    }
    if (!motion.prop_rot_dir) {
      return false;
    }
    return true;
  }
}
class ArrowCoordinateSystemService {
  /**
   * Pure service for coordinate system management and initial position calculation.
   *
   * Manages the TKA coordinate systems without any UI dependencies.
   * Provides precise coordinate mappings for different arrow types.
   */
  // Scene dimensions: 950x950 scene with center at (475, 475)
  SCENE_SIZE = 950;
  CENTER_X = 475;
  CENTER_Y = 475;
  // Hand point coordinates (for STATIC/DASH arrows)
  // These are the inner grid positions where props are placed
  HAND_POINTS = {
    [Location.NORTH]: { x: 475, y: 331.9 },
    [Location.EAST]: { x: 618.1, y: 475 },
    [Location.SOUTH]: { x: 475, y: 618.1 },
    [Location.WEST]: { x: 331.9, y: 475 },
    // Diagonal hand points (calculated from radius)
    [Location.NORTHEAST]: { x: 618.1, y: 331.9 },
    [Location.SOUTHEAST]: { x: 618.1, y: 618.1 },
    [Location.SOUTHWEST]: { x: 331.9, y: 618.1 },
    [Location.NORTHWEST]: { x: 331.9, y: 331.9 }
  };
  // Layer2 point coordinates (for PRO/ANTI/FLOAT arrows)
  // Using DIAMOND layer2 points from circle_coords.json
  LAYER2_POINTS = {
    // Diamond layer2 points are diagonal positions
    [Location.NORTHEAST]: { x: 618.1, y: 331.9 },
    [Location.SOUTHEAST]: { x: 618.1, y: 618.1 },
    [Location.SOUTHWEST]: { x: 331.9, y: 618.1 },
    [Location.NORTHWEST]: { x: 331.9, y: 331.9 },
    // For cardinal directions, map to nearest diagonal
    [Location.NORTH]: { x: 618.1, y: 331.9 },
    // Maps to NE
    [Location.EAST]: { x: 618.1, y: 618.1 },
    // Maps to SE
    [Location.SOUTH]: { x: 331.9, y: 618.1 },
    // Maps to SW
    [Location.WEST]: { x: 331.9, y: 331.9 }
    // Maps to NW
  };
  getInitialPosition(motion, location) {
    const motionType = motion.motion_type?.toLowerCase();
    if (["pro", "anti", "float"].includes(motionType || "")) {
      return this.getLayer2Coords(location);
    } else if (["static", "dash"].includes(motionType || "")) {
      return this.getHandPointCoords(location);
    } else {
      console.warn(`Unknown motion type: ${motionType}, using center`);
      return this.getSceneCenter();
    }
  }
  getSceneCenter() {
    return { x: this.CENTER_X, y: this.CENTER_Y };
  }
  getLayer2Coords(location) {
    const coords = this.LAYER2_POINTS[location];
    if (!coords) {
      console.warn(
        `No layer2 coordinates for location: ${location}, using center`
      );
      return this.getSceneCenter();
    }
    return coords;
  }
  getHandPointCoords(location) {
    const coords = this.HAND_POINTS[location];
    if (!coords) {
      console.warn(
        `No hand point coordinates for location: ${location}, using center`
      );
      return this.getSceneCenter();
    }
    return coords;
  }
  getSceneDimensions() {
    return [this.SCENE_SIZE, this.SCENE_SIZE];
  }
  getCoordinateInfo(location) {
    const handPoint = this.HAND_POINTS[location];
    const layer2Point = this.LAYER2_POINTS[location];
    return {
      location,
      hand_point: {
        x: handPoint?.x || null,
        y: handPoint?.y || null
      },
      layer2_point: {
        x: layer2Point?.x || null,
        y: layer2Point?.y || null
      },
      scene_center: { x: this.CENTER_X, y: this.CENTER_Y },
      scene_size: this.SCENE_SIZE
    };
  }
  validateCoordinates(point) {
    return point && typeof point.x === "number" && typeof point.y === "number" && point.x >= 0 && point.x <= this.SCENE_SIZE && point.y >= 0 && point.y <= this.SCENE_SIZE;
  }
  getAllHandPoints() {
    return { ...this.HAND_POINTS };
  }
  getAllLayer2Points() {
    return { ...this.LAYER2_POINTS };
  }
  getSupportedLocations() {
    return [
      Location.NORTH,
      Location.EAST,
      Location.SOUTH,
      Location.WEST,
      Location.NORTHEAST,
      Location.SOUTHEAST,
      Location.SOUTHWEST,
      Location.NORTHWEST
    ];
  }
}
class ArrowPositioningOrchestrator {
  /**
   * Orchestrator that coordinates all positioning microservices.
   *
   * Uses:
   * - ArrowLocationCalculator: Sophisticated location calculation with special cases
   * - ArrowRotationCalculator: Comprehensive rotation calculation with all motion types
   * - ArrowAdjustmentCalculator: Complex adjustment calculation with special/default placement
   * - ArrowCoordinateSystemService: Precise TKA coordinate system management
   */
  locationCalculator;
  rotationCalculator;
  adjustmentCalculator;
  coordinateSystem;
  mirrorConditions = {
    anti: { cw: true, ccw: false },
    other: { cw: false, ccw: true }
  };
  constructor(locationCalculator, rotationCalculator, adjustmentCalculator, coordinateSystem) {
    this.locationCalculator = locationCalculator;
    this.rotationCalculator = rotationCalculator;
    this.adjustmentCalculator = adjustmentCalculator;
    this.coordinateSystem = coordinateSystem;
  }
  // Main async method for full positioning calculation
  async calculateArrowPositionAsync(arrowData, pictographData, motionData) {
    try {
      const motion = motionData || this.getMotionFromPictograph(arrowData, pictographData);
      if (!motion) {
        console.warn(
          `No motion data for ${arrowData.color}, returning center position`
        );
        const center = this.coordinateSystem.getSceneCenter();
        return [center.x, center.y, 0];
      }
      const letter = pictographData.letter || "";
      const location = this.locationCalculator.calculateLocation(
        motion,
        pictographData
      );
      console.debug(
        `Calculated location: ${location} for ${arrowData.color} ${motion.motion_type}`
      );
      let initialPosition = this.coordinateSystem.getInitialPosition(
        motion,
        location
      );
      initialPosition = this.ensureValidPosition(initialPosition);
      console.debug(
        `Initial position: (${initialPosition.x}, ${initialPosition.y})`
      );
      const rotation = this.rotationCalculator.calculateRotation(
        motion,
        location
      );
      console.debug(
        `Calculated rotation: ${rotation}° for ${motion.motion_type} ${motion.prop_rot_dir}`
      );
      const adjustment = await this.adjustmentCalculator.calculateAdjustment(
        pictographData,
        motion,
        letter,
        location,
        arrowData.color
      );
      console.debug(
        `Calculated adjustment: (${adjustment.x}, ${adjustment.y})`
      );
      const [adjustmentX, adjustmentY] = this.extractAdjustmentValues(adjustment);
      const finalX = initialPosition.x + adjustmentX;
      const finalY = initialPosition.y + adjustmentY;
      return [finalX, finalY, rotation];
    } catch (error) {
      console.error("Arrow positioning failed:", error);
      const center = this.coordinateSystem.getSceneCenter();
      return [center.x, center.y, 0];
    }
  }
  // Synchronous version implementing IArrowPositioningOrchestrator interface
  calculateArrowPosition(arrowData, pictographData, motionData) {
    try {
      const motion = motionData || this.getMotionFromPictograph(arrowData, pictographData);
      if (!motion) {
        console.warn(
          `No motion data for ${arrowData.color}, returning center position`
        );
        const center = this.coordinateSystem.getSceneCenter();
        return [center.x, center.y, 0];
      }
      const letter = pictographData.letter || "";
      const location = this.locationCalculator.calculateLocation(
        motion,
        pictographData
      );
      let initialPosition = this.coordinateSystem.getInitialPosition(
        motion,
        location
      );
      initialPosition = this.ensureValidPosition(initialPosition);
      const rotation = this.rotationCalculator.calculateRotation(
        motion,
        location
      );
      const adjustment = this.adjustmentCalculator.calculateAdjustmentSync(
        pictographData,
        motion,
        letter,
        location,
        arrowData.color
      );
      const [adjustmentX, adjustmentY] = this.extractAdjustmentValues(adjustment);
      const finalX = initialPosition.x + adjustmentX;
      const finalY = initialPosition.y + adjustmentY;
      return [finalX, finalY, rotation];
    } catch (error) {
      console.error("Synchronous arrow positioning failed:", error);
      const center = this.coordinateSystem.getSceneCenter();
      return [center.x, center.y, 0];
    }
  }
  calculateAllArrowPositions(pictographData) {
    let updatedPictograph = pictographData;
    try {
      if (!pictographData.arrows) {
        return updatedPictograph;
      }
      for (const [color, arrowData] of Object.entries(pictographData.arrows)) {
        const motionData = pictographData.motions?.[color];
        if (arrowData.is_visible && motionData) {
          const [x, y, rotation] = this.calculateArrowPositionSync(
            arrowData,
            pictographData,
            motionData
          );
          const shouldMirror = this.shouldMirrorArrow(
            arrowData,
            pictographData
          );
          updatedPictograph = this.updateArrowInPictograph(
            updatedPictograph,
            color,
            {
              position_x: x,
              position_y: y,
              rotation_angle: rotation,
              is_mirrored: shouldMirror
            }
          );
          console.log(
            `Updated ${color} arrow: position=(${x}, ${y}), rotation=${rotation}°, mirrored=${shouldMirror}`
          );
        }
      }
    } catch (error) {
      console.error("Failed to calculate all arrow positions:", error);
    }
    return updatedPictograph;
  }
  shouldMirrorArrow(arrowData, pictographData) {
    try {
      let motion;
      if (pictographData?.motions) {
        motion = pictographData.motions[arrowData.color];
      }
      if (!motion) {
        return false;
      }
      const motionType = (motion.motion_type || "").toLowerCase();
      const propRotDir = (motion.prop_rot_dir || "").toLowerCase();
      if (motionType === "anti") {
        return this.mirrorConditions.anti[propRotDir] || false;
      }
      return this.mirrorConditions.other[propRotDir] || false;
    } catch (error) {
      console.warn("Mirror calculation failed, using default:", error);
      return false;
    }
  }
  applyMirrorTransform(arrowItem, shouldMirror) {
    try {
      if (shouldMirror) {
        const rect = arrowItem.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        const scaleX = -1;
        const transform = `translate(${centerX}px, ${centerY}px) scale(${scaleX}, 1) translate(${-centerX}px, ${-centerY}px)`;
        arrowItem.style.transform = transform;
      } else {
        arrowItem.style.transform = "";
      }
    } catch (error) {
      console.warn("Failed to apply mirror transform:", error);
    }
  }
  // Private helper methods
  calculateArrowPositionSync(_arrowData, _pictographData, motionData) {
    const motion = motionData;
    const letter = _pictographData.letter || "";
    const location = this.locationCalculator.calculateLocation(
      motion,
      _pictographData
    );
    let initialPosition = this.coordinateSystem.getInitialPosition(
      motion,
      location
    );
    initialPosition = this.ensureValidPosition(initialPosition);
    const rotation = this.rotationCalculator.calculateRotation(
      motion,
      location
    );
    const adjustment = this.getBasicAdjustment(motion, letter);
    const [adjustmentX, adjustmentY] = this.extractAdjustmentValues(adjustment);
    const finalX = initialPosition.x + adjustmentX;
    const finalY = initialPosition.y + adjustmentY;
    return [finalX, finalY, rotation];
  }
  getMotionFromPictograph(arrowData, pictographData) {
    if (!pictographData?.motions) {
      return void 0;
    }
    return pictographData.motions[arrowData.color];
  }
  ensureValidPosition(initialPosition) {
    if (initialPosition && typeof initialPosition.x === "number" && typeof initialPosition.y === "number") {
      return initialPosition;
    }
    console.warn("Invalid initial position, using scene center");
    return this.coordinateSystem.getSceneCenter();
  }
  extractAdjustmentValues(adjustment) {
    if (typeof adjustment === "number") {
      return [adjustment, adjustment];
    }
    if (adjustment && typeof adjustment.x === "number" && typeof adjustment.y === "number") {
      return [adjustment.x, adjustment.y];
    }
    return [0, 0];
  }
  getBasicAdjustment(motion, _letter) {
    try {
      const location = this.locationCalculator.calculateLocation(motion, {
        letter: _letter
      });
      const baseAdjustment = this.getBaseAdjustmentValues(motion);
      const finalAdjustment = this.processDirectionalTuples(
        baseAdjustment,
        motion,
        location
      );
      console.debug(
        `Basic adjustment for ${motion.motion_type} ${motion.turns} turns at ${location}: (${finalAdjustment.x}, ${finalAdjustment.y})`
      );
      return finalAdjustment;
    } catch (error) {
      console.warn("Basic adjustment calculation failed:", error);
      return { x: 0, y: 0 };
    }
  }
  getBaseAdjustmentValues(motion) {
    const motionType = motion.motion_type;
    const turns = typeof motion.turns === "number" ? motion.turns : 0;
    const turnsStr = turns === Math.floor(turns) ? turns.toString() : turns.toString();
    const defaultAdjustments = {
      pro: {
        "0": [-10, -40],
        "0.5": [30, 105],
        "1": [30, 25],
        "1.5": [-35, 145],
        "2": [-10, -35],
        "2.5": [20, 100],
        "3": [30, 25]
      },
      anti: {
        "0": [0, -40],
        "0.5": [-15, 110],
        "1": [0, -40],
        "1.5": [20, 155],
        "2": [0, -40],
        "2.5": [0, 100],
        "3": [0, -50]
      },
      static: {
        "0": [0, 0]
      },
      dash: {
        "0": [0, 0]
      },
      float: {
        "0": [0, 0]
      }
    };
    const motionAdjustments = defaultAdjustments[motionType];
    if (motionAdjustments && motionAdjustments[turnsStr]) {
      const [x, y] = motionAdjustments[turnsStr];
      return { x, y };
    }
    return { x: 0, y: 0 };
  }
  processDirectionalTuples(baseAdjustment, motion, location) {
    try {
      const directionalTuples = this.generateDirectionalTuples(
        motion,
        baseAdjustment.x,
        baseAdjustment.y
      );
      const quadrantIndex = this.calculateQuadrantIndex(location);
      const selectedTuple = directionalTuples[quadrantIndex] || [0, 0];
      console.debug(
        `Directional tuples: ${JSON.stringify(directionalTuples)}, quadrant: ${quadrantIndex}, selected: [${selectedTuple[0]}, ${selectedTuple[1]}]`
      );
      return { x: selectedTuple[0], y: selectedTuple[1] };
    } catch (error) {
      console.warn(
        "Directional tuple processing failed, using base adjustment:",
        error
      );
      return baseAdjustment;
    }
  }
  generateDirectionalTuples(motion, baseX, baseY) {
    const motionType = motion.motion_type;
    const rotationDir = motion.prop_rot_dir;
    const rotationStr = rotationDir === RotationDirection.CLOCKWISE ? "clockwise" : rotationDir === RotationDirection.COUNTER_CLOCKWISE ? "counter_clockwise" : "clockwise";
    const shiftMappingDiamond = {
      [MotionType.PRO]: {
        clockwise: (x, y) => [
          [x, y],
          // NE (0)
          [-y, x],
          // SE (1)
          [-x, -y],
          // SW (2)
          [y, -x]
          // NW (3)
        ],
        counter_clockwise: (x, y) => [
          [-y, -x],
          // NE (0)
          [x, -y],
          // SE (1)
          [y, x],
          // SW (2)
          [-x, y]
          // NW (3)
        ]
      },
      [MotionType.ANTI]: {
        clockwise: (x, y) => [
          [-y, -x],
          // NE (0)
          [x, -y],
          // SE (1)
          [y, x],
          // SW (2)
          [-x, y]
          // NW (3)
        ],
        counter_clockwise: (x, y) => [
          [x, y],
          // NE (0)
          [-y, x],
          // SE (1)
          [-x, -y],
          // SW (2)
          [y, -x]
          // NW (3)
        ]
      }
    };
    if (motionType === MotionType.STATIC || motionType === MotionType.DASH || motionType === MotionType.FLOAT) {
      return [
        [baseX, baseY],
        [-baseX, -baseY],
        [-baseY, baseX],
        [baseY, -baseX]
      ];
    }
    const mapping = shiftMappingDiamond[motionType];
    if (mapping && mapping[rotationStr]) {
      const transformFunc = mapping[rotationStr];
      return transformFunc(baseX, baseY);
    }
    return [
      [baseX, baseY],
      [baseX, baseY],
      [baseX, baseY],
      [baseX, baseY]
    ];
  }
  calculateQuadrantIndex(location) {
    const quadrantMap = {
      [Location.NORTHEAST]: 0,
      [Location.SOUTHEAST]: 1,
      [Location.SOUTHWEST]: 2,
      [Location.NORTHWEST]: 3,
      // Cardinal directions map to nearest quadrant
      [Location.NORTH]: 0,
      // Maps to NE quadrant
      [Location.EAST]: 1,
      // Maps to SE quadrant
      [Location.SOUTH]: 2,
      // Maps to SW quadrant
      [Location.WEST]: 3
      // Maps to NW quadrant
    };
    return quadrantMap[location] || 0;
  }
  updateArrowInPictograph(pictographData, color, updates) {
    const updatedPictograph = { ...pictographData };
    if (updatedPictograph.arrows && updatedPictograph.arrows[color]) {
      updatedPictograph.arrows = {
        ...updatedPictograph.arrows,
        [color]: {
          ...updatedPictograph.arrows[color],
          ...updates
        }
      };
    }
    return updatedPictograph;
  }
}
class PositioningServiceFactory {
  /**
   * Factory for creating the complete positioning service ecosystem.
   *
   * Creates all services with proper dependency injection and ensures
   * they are wired together correctly for optimal positioning accuracy.
   */
  static instance;
  // Singleton services (shared across all arrows)
  dashLocationCalculator;
  coordinateSystemService;
  specialPlacementService;
  defaultPlacementService;
  directionalTupleProcessor;
  /**
   * Get the singleton instance of the positioning service factory.
   */
  static getInstance() {
    if (!PositioningServiceFactory.instance) {
      PositioningServiceFactory.instance = new PositioningServiceFactory();
    }
    return PositioningServiceFactory.instance;
  }
  createLocationCalculator() {
    if (!this.dashLocationCalculator) {
      this.dashLocationCalculator = this.createDashLocationCalculator();
    }
    return new ArrowLocationCalculator(this.dashLocationCalculator);
  }
  createRotationCalculator() {
    return new ArrowRotationCalculator();
  }
  createAdjustmentCalculator() {
    if (!this.specialPlacementService) {
      this.specialPlacementService = new SpecialPlacementService();
    }
    if (!this.defaultPlacementService) {
      this.defaultPlacementService = new DefaultPlacementService();
    }
    if (!this.directionalTupleProcessor) {
      this.directionalTupleProcessor = this.createDirectionalTupleProcessor();
    }
    const lookupService = new ArrowAdjustmentLookup(
      this.specialPlacementService,
      this.defaultPlacementService,
      new SpecialPlacementOriKeyGenerator(),
      new PlacementKeyGenerator(),
      new TurnsTupleKeyGenerator(),
      new AttributeKeyGenerator()
    );
    return new ArrowAdjustmentCalculator(
      lookupService,
      // Use cached placement services
      this.directionalTupleProcessor
    );
  }
  createCoordinateSystemService() {
    if (!this.coordinateSystemService) {
      this.coordinateSystemService = new ArrowCoordinateSystemService();
    }
    return this.coordinateSystemService;
  }
  createDashLocationCalculator() {
    if (!this.dashLocationCalculator) {
      this.dashLocationCalculator = new DashLocationCalculator();
    }
    return this.dashLocationCalculator;
  }
  createDirectionalTupleProcessor() {
    if (!this.directionalTupleProcessor) {
      const directionalTupleCalculator = new DirectionalTupleCalculator();
      const quadrantIndexCalculator = new QuadrantIndexCalculator();
      this.directionalTupleProcessor = new DirectionalTupleProcessor(
        directionalTupleCalculator,
        quadrantIndexCalculator
      );
    }
    return this.directionalTupleProcessor;
  }
  createPositioningOrchestrator() {
    const locationCalculator = this.createLocationCalculator();
    const rotationCalculator = this.createRotationCalculator();
    const adjustmentCalculator = this.createAdjustmentCalculator();
    const coordinateSystemService = this.createCoordinateSystemService();
    return new ArrowPositioningOrchestrator(
      locationCalculator,
      rotationCalculator,
      adjustmentCalculator,
      coordinateSystemService
    );
  }
  /**
   * Create a complete positioning pipeline for use in services.
   * Returns all the key services needed for positioning operations.
   */
  createPositioningPipeline() {
    return {
      locationCalculator: this.createLocationCalculator(),
      rotationCalculator: this.createRotationCalculator(),
      adjustmentCalculator: this.createAdjustmentCalculator(),
      coordinateSystemService: this.createCoordinateSystemService(),
      orchestrator: this.createPositioningOrchestrator()
    };
  }
  /**
   * Reset all singleton services (useful for testing).
   */
  resetServices() {
    this.dashLocationCalculator = void 0;
    this.coordinateSystemService = void 0;
    this.specialPlacementService = void 0;
    this.defaultPlacementService = void 0;
    this.directionalTupleProcessor = void 0;
  }
  /**
   * Pre-warm all services by creating them in advance.
   * Useful for ensuring consistent performance.
   */
  async preWarmServices() {
    console.log("Pre-warming positioning services...");
    this.createLocationCalculator();
    this.createRotationCalculator();
    this.createCoordinateSystemService();
    this.createDirectionalTupleProcessor();
    if (!this.defaultPlacementService) {
      this.defaultPlacementService = new DefaultPlacementService();
    }
    if (!this.defaultPlacementService.isLoaded()) {
      try {
        await this.defaultPlacementService.debugAvailableKeys(
          MotionType.PRO,
          GridMode.DIAMOND
        );
        console.log("✅ Positioning services pre-warmed successfully");
      } catch (error) {
        console.warn("⚠️ Some positioning services failed to pre-warm:", error);
      }
    }
  }
}
function getPositioningServiceFactory() {
  return PositioningServiceFactory.getInstance();
}
const IArrowPlacementDataServiceInterface = createServiceInterface$1(
  "IArrowPlacementDataService",
  ArrowPlacementDataService
);
const IArrowPlacementKeyServiceInterface = createServiceInterface$1(
  "IArrowPlacementKeyService",
  ArrowPlacementKeyService
);
const IArrowPositioningServiceInterface = createServiceInterface$1(
  "IArrowPositioningService",
  class extends ArrowPositioningService$1 {
    constructor(...args) {
      super(
        args[0],
        args[1]
      );
    }
  }
);
const IArrowLocationCalculatorInterface = createServiceInterface$1(
  "IArrowLocationCalculator",
  class extends ArrowLocationCalculator {
    constructor(...args) {
      super(args[0]);
    }
  }
);
const IArrowRotationCalculatorInterface = createServiceInterface$1(
  "IArrowRotationCalculator",
  ArrowRotationCalculator
);
const IArrowAdjustmentCalculatorInterface = createServiceInterface$1(
  "IArrowAdjustmentCalculator",
  class extends ArrowAdjustmentCalculator {
    constructor(...args) {
      super(
        args[0],
        args[1]
      );
    }
  }
);
const IArrowCoordinateSystemServiceInterface = createServiceInterface$1(
  "IArrowCoordinateSystemService",
  ArrowCoordinateSystemService
);
const IDashLocationCalculatorInterface = createServiceInterface$1(
  "IDashLocationCalculator",
  DashLocationCalculator
);
const IDirectionalTupleProcessorInterface = createServiceInterface$1(
  "IDirectionalTupleProcessor",
  class extends DirectionalTupleProcessor {
    constructor(...args) {
      super(
        args[0],
        args[1]
      );
    }
  }
);
const IArrowPositioningOrchestratorInterface = createServiceInterface$1(
  "IArrowPositioningOrchestrator",
  class extends ArrowPositioningOrchestrator {
    constructor(...args) {
      super(
        args[0],
        args[1],
        args[2],
        args[3]
      );
    }
  }
);
const IPositioningServiceFactoryInterface = createServiceInterface$1(
  "IPositioningServiceFactory",
  PositioningServiceFactory
);
class BrowseService {
  cachedSequences = null;
  async loadSequenceMetadata() {
    console.log("🔍 BrowseService.loadSequenceMetadata() called");
    if (this.cachedSequences !== null) {
      console.log(
        "📦 Returning cached sequences:",
        this.cachedSequences.length,
        "items"
      );
      return this.cachedSequences;
    }
    try {
      console.log("🔄 Loading from sequence index...");
      const sequences = await this.loadFromSequenceIndex();
      console.log(
        "✅ Successfully loaded from sequence index:",
        sequences.length,
        "sequences"
      );
      console.log(
        "📋 Sequence IDs:",
        sequences.map((s) => s.id)
      );
      this.cachedSequences = sequences;
      return sequences;
    } catch (error) {
      console.warn(
        "❌ Failed to load sequence index, generating from dictionary:",
        error
      );
      const sequences = await this.generateSequenceIndex();
      console.log(
        "🔧 Generated sequences as fallback:",
        sequences.length,
        "sequences"
      );
      this.cachedSequences = sequences;
      return sequences;
    }
  }
  async applyFilter(sequences, filterType, filterValue) {
    console.log("🔍 BrowseService.applyFilter() called with:");
    console.log("  - filterType:", filterType);
    console.log("  - filterValue:", filterValue);
    console.log("  - input sequences:", sequences.length, "items");
    if (filterType === FilterType.ALL_SEQUENCES) {
      console.log(
        "✅ ALL_SEQUENCES filter detected - returning all sequences:",
        sequences.length
      );
      return sequences;
    }
    console.log("🔄 Applying specific filter...");
    let filtered;
    switch (filterType) {
      case FilterType.STARTING_LETTER:
        filtered = this.filterByStartingLetter(sequences, filterValue);
        break;
      case FilterType.CONTAINS_LETTERS:
        filtered = this.filterByContainsLetters(sequences, filterValue);
        break;
      case FilterType.LENGTH:
        filtered = this.filterByLength(sequences, filterValue);
        break;
      case FilterType.DIFFICULTY:
        filtered = this.filterByDifficulty(sequences, filterValue);
        break;
      case FilterType.STARTING_POSITION:
        filtered = this.filterByStartingPosition(sequences, filterValue);
        break;
      case FilterType.AUTHOR:
        filtered = this.filterByAuthor(sequences, filterValue);
        break;
      case FilterType.GRID_MODE:
        filtered = this.filterByGridMode(sequences, filterValue);
        break;
      case FilterType.FAVORITES:
        filtered = sequences.filter((s) => s.isFavorite);
        break;
      case FilterType.RECENT:
        filtered = this.filterByRecent(sequences);
        break;
      default:
        console.log("⚠️ Unknown filter type, returning all sequences");
        filtered = sequences;
    }
    console.log(
      "📊 Filter result:",
      filtered.length,
      "sequences after filtering"
    );
    return filtered;
  }
  async sortSequences(sequences, sortMethod) {
    const sorted = [...sequences];
    switch (sortMethod) {
      case SortMethod.ALPHABETICAL:
        return sorted.sort((a, b) => a.word.localeCompare(b.word));
      case SortMethod.DATE_ADDED:
        return sorted.sort((a, b) => {
          const dateA = a.dateAdded || /* @__PURE__ */ new Date(0);
          const dateB = b.dateAdded || /* @__PURE__ */ new Date(0);
          return dateB.getTime() - dateA.getTime();
        });
      case SortMethod.DIFFICULTY_LEVEL:
        return sorted.sort((a, b) => {
          const levelA = this.getDifficultyOrder(a.difficultyLevel);
          const levelB = this.getDifficultyOrder(b.difficultyLevel);
          return levelA - levelB;
        });
      case SortMethod.SEQUENCE_LENGTH:
        return sorted.sort(
          (a, b) => (a.sequenceLength || 0) - (b.sequenceLength || 0)
        );
      case SortMethod.AUTHOR:
        return sorted.sort(
          (a, b) => (a.author || "").localeCompare(b.author || "")
        );
      case SortMethod.POPULARITY:
        return sorted.sort(
          (a, b) => Number(b.isFavorite) - Number(a.isFavorite)
        );
      default:
        return sorted;
    }
  }
  async groupSequencesIntoSections(sequences, sortMethod) {
    const sections = {};
    for (const sequence of sequences) {
      const sectionKey = this.getSectionKey(sequence, sortMethod);
      if (!sections[sectionKey]) {
        sections[sectionKey] = [];
      }
      sections[sectionKey].push(sequence);
    }
    return sections;
  }
  async getUniqueValues(field) {
    const sequences = await this.loadSequenceMetadata();
    const values = /* @__PURE__ */ new Set();
    for (const sequence of sequences) {
      const value = sequence[field];
      if (value != null) {
        values.add(String(value));
      }
    }
    return Array.from(values).sort();
  }
  async getFilterOptions(filterType) {
    switch (filterType) {
      case FilterType.STARTING_LETTER:
        return ["A-D", "E-H", "I-L", "M-P", "Q-T", "U-Z"];
      case FilterType.LENGTH:
        return ["3", "4", "5", "6", "7", "8+"];
      case FilterType.DIFFICULTY:
        return ["beginner", "intermediate", "advanced"];
      case FilterType.AUTHOR:
        return this.getUniqueValues("author");
      case FilterType.GRID_MODE:
        return ["diamond", "box"];
      default:
        return [];
    }
  }
  // Private helper methods
  async loadFromSequenceIndex() {
    console.log("🌐 Fetching sequence-index.json...");
    const response = await fetch("/sequence-index.json");
    console.log("🌐 Response status:", response.status, response.statusText);
    if (!response.ok) {
      throw new Error(`Failed to load sequence index: ${response.status}`);
    }
    const data = await response.json();
    console.log("📄 Loaded sequence index data:", data);
    console.log("📄 Total sequences in index:", data.totalSequences);
    console.log("📄 Sequences array length:", data.sequences?.length || 0);
    const sequences = data.sequences || [];
    console.log("📦 Returning sequences:", sequences.length, "items");
    return sequences;
  }
  async generateSequenceIndex() {
    return this.createSampleSequences();
  }
  createSampleSequences() {
    const sampleWords = [
      "ALPHA",
      "BETA",
      "GAMMA",
      "DELTA",
      "EPSILON",
      "ZETA",
      "ETA",
      "THETA",
      "IOTA",
      "KAPPA",
      "LAMBDA",
      "MU",
      "NU",
      "XI",
      "OMICRON",
      "PI",
      "RHO",
      "SIGMA"
    ];
    const authors = ["TKA User", "Demo Author", "Expert User"];
    const difficulties = ["beginner", "intermediate", "advanced"];
    const gridModes = ["diamond", "box"];
    return sampleWords.map((word, index) => {
      const authorValue = authors[index % authors.length];
      const gridModeValue = gridModes[index % gridModes.length];
      const difficultyValue = difficulties[index % difficulties.length];
      const result = {
        id: word.toLowerCase(),
        name: `${word} Sequence`,
        word,
        thumbnails: [`${word}_ver1.png`],
        isFavorite: Math.random() > 0.7,
        isCircular: false,
        tags: ["flow", "practice"],
        metadata: { generated: true }
      };
      if (authorValue) result.author = authorValue;
      if (gridModeValue) result.gridMode = gridModeValue;
      if (difficultyValue) result.difficultyLevel = difficultyValue;
      result.sequenceLength = Math.floor(Math.random() * 8) + 3;
      result.level = Math.floor(Math.random() * 4) + 1;
      result.dateAdded = new Date(
        Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1e3
      );
      result.propType = "fans";
      result.startingPosition = "center";
      return result;
    });
  }
  filterByStartingLetter(sequences, filterValue) {
    if (!filterValue || typeof filterValue !== "string") return sequences;
    if (filterValue.includes("-")) {
      const [start, end] = filterValue.split("-");
      return sequences.filter((s) => {
        const firstLetter = s.word[0]?.toUpperCase();
        return firstLetter && start && end && firstLetter >= start && firstLetter <= end;
      });
    }
    return sequences.filter(
      (s) => s.word[0]?.toUpperCase() === filterValue.toUpperCase()
    );
  }
  filterByContainsLetters(sequences, filterValue) {
    if (!filterValue || typeof filterValue !== "string") return sequences;
    return sequences.filter(
      (s) => s.word.toLowerCase().includes(filterValue.toLowerCase())
    );
  }
  filterByLength(sequences, filterValue) {
    if (!filterValue) return sequences;
    if (filterValue === "8+") {
      return sequences.filter((s) => (s.sequenceLength || 0) >= 8);
    }
    const length = parseInt(String(filterValue));
    if (isNaN(length)) return sequences;
    return sequences.filter((s) => s.sequenceLength === length);
  }
  filterByDifficulty(sequences, filterValue) {
    if (!filterValue) return sequences;
    return sequences.filter((s) => s.difficultyLevel === filterValue);
  }
  filterByStartingPosition(sequences, filterValue) {
    if (!filterValue) return sequences;
    return sequences.filter((s) => s.startingPosition === filterValue);
  }
  filterByAuthor(sequences, filterValue) {
    if (!filterValue) return sequences;
    return sequences.filter((s) => s.author === filterValue);
  }
  filterByGridMode(sequences, filterValue) {
    if (!filterValue) return sequences;
    return sequences.filter((s) => s.gridMode === filterValue);
  }
  filterByRecent(sequences) {
    const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1e3);
    return sequences.filter((s) => {
      const dateAdded = s.dateAdded || /* @__PURE__ */ new Date(0);
      return dateAdded >= thirtyDaysAgo;
    });
  }
  getDifficultyOrder(difficulty) {
    switch (difficulty) {
      case "beginner":
        return 1;
      case "intermediate":
        return 2;
      case "advanced":
        return 3;
      default:
        return 0;
    }
  }
  getSectionKey(sequence, sortMethod) {
    switch (sortMethod) {
      case SortMethod.ALPHABETICAL:
        return sequence.word[0]?.toUpperCase() || "#";
      case SortMethod.DIFFICULTY_LEVEL:
        return sequence.difficultyLevel || "Unknown";
      case SortMethod.AUTHOR:
        return sequence.author || "Unknown";
      case SortMethod.SEQUENCE_LENGTH: {
        const length = sequence.sequenceLength || 0;
        if (length <= 4) return "3-4 beats";
        if (length <= 6) return "5-6 beats";
        if (length <= 8) return "7-8 beats";
        return "9+ beats";
      }
      default:
        return "All";
    }
  }
  clearCache() {
    this.cachedSequences = null;
  }
}
class DeleteService {
  async prepareDeleteConfirmation(sequence, allSequences) {
    const relatedSequences = this.findRelatedSequences(sequence, allSequences);
    const hasVariations = relatedSequences.length > 0;
    const willFixVariationNumbers = hasVariations && this.needsVariationNumberFix(sequence, relatedSequences);
    return {
      sequence,
      relatedSequences,
      hasVariations,
      willFixVariationNumbers
    };
  }
  async deleteSequence(sequenceId, allSequences) {
    try {
      const sequence = allSequences.find((seq) => seq.id === sequenceId);
      if (!sequence) {
        return {
          success: false,
          deletedSequence: null,
          affectedSequences: [],
          error: "Sequence not found"
        };
      }
      const canDelete = await this.canDeleteSequence(sequence, allSequences);
      if (!canDelete) {
        return {
          success: false,
          deletedSequence: null,
          affectedSequences: [],
          error: "Sequence cannot be deleted"
        };
      }
      const affectedSequences = await this.getAffectedSequences(
        sequence,
        allSequences
      );
      const updatedSequences = await this.fixVariationNumbers(
        sequence,
        allSequences
      );
      console.log(`Deleting sequence: ${sequence.word} (${sequence.id})`);
      const remainingSequences = updatedSequences.filter(
        (seq) => seq.id !== sequenceId
      );
      return {
        success: true,
        deletedSequence: sequence,
        affectedSequences: remainingSequences.filter(
          (seq) => affectedSequences.some((affected) => affected.id === seq.id)
        )
      };
    } catch (error) {
      return {
        success: false,
        deletedSequence: null,
        affectedSequences: [],
        error: error instanceof Error ? error.message : "Unknown error occurred"
      };
    }
  }
  async fixVariationNumbers(deletedSequence, allSequences) {
    const baseWord = this.extractBaseWord(deletedSequence.word);
    const deletedVariation = this.extractVariationNumber(deletedSequence.word);
    if (!deletedVariation) {
      return allSequences;
    }
    const updatedSequences = allSequences.map((sequence) => {
      if (sequence.id === deletedSequence.id) {
        return sequence;
      }
      const sequenceBaseWord = this.extractBaseWord(sequence.word);
      const sequenceVariation = this.extractVariationNumber(sequence.word);
      if (sequenceBaseWord === baseWord && sequenceVariation && sequenceVariation > deletedVariation) {
        const newVariationNumber = sequenceVariation - 1;
        const newWord = this.createWordWithVariation(
          baseWord,
          newVariationNumber
        );
        return {
          ...sequence,
          word: newWord,
          name: sequence.name.replace(sequence.word, newWord)
        };
      }
      return sequence;
    });
    return updatedSequences;
  }
  async canDeleteSequence(sequence, _allSequences) {
    const isProtected = sequence.metadata?.isProtected;
    const isSystem = sequence.metadata?.isSystem;
    if (isProtected || isSystem) {
      return false;
    }
    if (sequence.author && sequence.author !== "current-user") {
      return true;
    }
    return true;
  }
  async getAffectedSequences(sequence, allSequences) {
    const affected = [];
    const baseWord = this.extractBaseWord(sequence.word);
    const deletedVariation = this.extractVariationNumber(sequence.word);
    if (!deletedVariation) {
      return affected;
    }
    allSequences.forEach((seq) => {
      if (seq.id === sequence.id) return;
      const seqBaseWord = this.extractBaseWord(seq.word);
      const seqVariation = this.extractVariationNumber(seq.word);
      if (seqBaseWord === baseWord && seqVariation && seqVariation > deletedVariation) {
        affected.push(seq);
      }
    });
    return affected;
  }
  // Private helper methods
  findRelatedSequences(sequence, allSequences) {
    const baseWord = this.extractBaseWord(sequence.word);
    return allSequences.filter((seq) => {
      if (seq.id === sequence.id) return false;
      const seqBaseWord = this.extractBaseWord(seq.word);
      return seqBaseWord === baseWord;
    });
  }
  needsVariationNumberFix(deletedSequence, relatedSequences) {
    const deletedVariation = this.extractVariationNumber(deletedSequence.word);
    if (!deletedVariation) return false;
    return relatedSequences.some((seq) => {
      const variation = this.extractVariationNumber(seq.word);
      return variation && variation > deletedVariation;
    });
  }
  extractBaseWord(word) {
    const match = word.match(/^([A-Z]+)(?:[_-]v?(\d+))?$/i);
    return match && match[1] ? match[1] : word;
  }
  extractVariationNumber(word) {
    const match = word.match(/[_-]v?(\d+)$/i);
    return match && match[1] ? parseInt(match[1]) : null;
  }
  createWordWithVariation(baseWord, variation) {
    if (variation <= 1) {
      return baseWord;
    }
    return `${baseWord}_v${variation}`;
  }
  // Utility methods for UI components
  async formatDeleteConfirmationMessage(data) {
    const {
      sequence,
      relatedSequences,
      hasVariations,
      willFixVariationNumbers
    } = data;
    let message = `Are you sure you want to delete "${sequence.word}"?`;
    if (hasVariations) {
      message += `

This sequence has ${relatedSequences.length} related variation(s).`;
      if (willFixVariationNumbers) {
        message += "\nVariation numbers will be automatically updated to maintain sequence.";
      }
    }
    message += "\n\nThis action cannot be undone.";
    return message;
  }
  async getDeleteButtonText(data) {
    if (data.willFixVariationNumbers) {
      return "Delete & Fix Variations";
    }
    return "Delete Sequence";
  }
}
class FavoritesService {
  STORAGE_KEY = "tka-favorites";
  favoritesCache = null;
  constructor() {
    this.loadFavoritesFromStorage();
  }
  async toggleFavorite(sequenceId) {
    await this.ensureCacheLoaded();
    if (this.favoritesCache.has(sequenceId)) {
      this.favoritesCache.delete(sequenceId);
    } else {
      this.favoritesCache.add(sequenceId);
    }
    await this.saveFavoritesToStorage();
  }
  async isFavorite(sequenceId) {
    await this.ensureCacheLoaded();
    return this.favoritesCache.has(sequenceId);
  }
  async getFavorites() {
    await this.ensureCacheLoaded();
    return Array.from(this.favoritesCache);
  }
  async setFavorite(sequenceId, isFavorite) {
    await this.ensureCacheLoaded();
    if (isFavorite) {
      this.favoritesCache.add(sequenceId);
    } else {
      this.favoritesCache.delete(sequenceId);
    }
    await this.saveFavoritesToStorage();
  }
  async clearFavorites() {
    this.favoritesCache = /* @__PURE__ */ new Set();
    await this.saveFavoritesToStorage();
  }
  async getFavoritesCount() {
    await this.ensureCacheLoaded();
    return this.favoritesCache.size;
  }
  // Private methods
  async ensureCacheLoaded() {
    if (this.favoritesCache === null) {
      await this.loadFavoritesFromStorage();
    }
  }
  async loadFavoritesFromStorage() {
    try {
      const stored = sessionStorage.getItem(this.STORAGE_KEY);
      const favorites = stored ? JSON.parse(stored) : [];
      this.favoritesCache = new Set(favorites);
    } catch (error) {
      console.warn("Failed to load favorites from storage:", error);
      this.favoritesCache = /* @__PURE__ */ new Set();
    }
  }
  async saveFavoritesToStorage() {
    try {
      const favorites = Array.from(this.favoritesCache);
      sessionStorage.setItem(this.STORAGE_KEY, JSON.stringify(favorites));
    } catch (error) {
      console.error("Failed to save favorites to storage:", error);
    }
  }
}
class FilterPersistenceService {
  BROWSE_STATE_KEY = "tka-browse-state";
  FILTER_HISTORY_KEY = "tka-filter-history";
  MAX_HISTORY_SIZE = 50;
  async saveBrowseState(state) {
    try {
      const stateToSave = {
        ...state,
        lastUpdated: /* @__PURE__ */ new Date()
      };
      sessionStorage.setItem(
        this.BROWSE_STATE_KEY,
        JSON.stringify(stateToSave)
      );
    } catch (error) {
      console.error("Failed to save browse state:", error);
    }
  }
  async loadBrowseState() {
    try {
      const saved = sessionStorage.getItem(this.BROWSE_STATE_KEY);
      if (!saved) return null;
      const parsed = JSON.parse(saved);
      if (parsed.currentFilter?.appliedAt) {
        parsed.currentFilter.appliedAt = new Date(
          parsed.currentFilter.appliedAt
        );
      }
      if (parsed.lastUpdated) {
        parsed.lastUpdated = new Date(parsed.lastUpdated);
      }
      const oneDay = 24 * 60 * 60 * 1e3;
      if (parsed.lastUpdated && Date.now() - parsed.lastUpdated.getTime() > oneDay) {
        return null;
      }
      return parsed;
    } catch (error) {
      console.warn("Failed to load browse state:", error);
      return null;
    }
  }
  async saveFilterToHistory(filter) {
    try {
      const history = await this.getFilterHistory();
      const filteredHistory = history.filter(
        (f) => !(f.type === filter.type && JSON.stringify(f.value) === JSON.stringify(filter.value))
      );
      const newHistory = [filter, ...filteredHistory];
      const trimmedHistory = newHistory.slice(0, this.MAX_HISTORY_SIZE);
      sessionStorage.setItem(
        this.FILTER_HISTORY_KEY,
        JSON.stringify(trimmedHistory)
      );
    } catch (error) {
      console.error("Failed to save filter to history:", error);
    }
  }
  async getFilterHistory() {
    try {
      const saved = sessionStorage.getItem(this.FILTER_HISTORY_KEY);
      if (!saved) return [];
      const parsed = JSON.parse(saved);
      return parsed.map(
        (filter) => ({
          ...filter,
          appliedAt: new Date(filter.appliedAt)
        })
      );
    } catch (error) {
      console.warn("Failed to load filter history:", error);
      return [];
    }
  }
  async clearFilterHistory() {
    try {
      sessionStorage.removeItem(this.FILTER_HISTORY_KEY);
    } catch (error) {
      console.error("Failed to clear filter history:", error);
    }
  }
  async getRecentFilters(limit = 10) {
    const history = await this.getFilterHistory();
    return history.slice(0, limit);
  }
  async clearAllState() {
    try {
      sessionStorage.removeItem(this.BROWSE_STATE_KEY);
      sessionStorage.removeItem(this.FILTER_HISTORY_KEY);
    } catch (error) {
      console.error("Failed to clear all state:", error);
    }
  }
  // Utility methods for filter management
  async getFilterFrequency() {
    const history = await this.getFilterHistory();
    const frequency = /* @__PURE__ */ new Map();
    history.forEach((filter) => {
      const key = `${filter.type}:${JSON.stringify(filter.value)}`;
      frequency.set(key, (frequency.get(key) || 0) + 1);
    });
    return frequency;
  }
  async getMostUsedFilters(limit = 5) {
    const history = await this.getFilterHistory();
    const frequency = await this.getFilterFrequency();
    const filterMap = /* @__PURE__ */ new Map();
    history.forEach((filter) => {
      const key = `${filter.type}:${JSON.stringify(filter.value)}`;
      if (!filterMap.has(key)) {
        filterMap.set(key, filter);
      }
    });
    return Array.from(filterMap.values()).sort((a, b) => {
      const keyA = `${a.type}:${JSON.stringify(a.value)}`;
      const keyB = `${b.type}:${JSON.stringify(b.value)}`;
      return (frequency.get(keyB) || 0) - (frequency.get(keyA) || 0);
    }).slice(0, limit);
  }
  async getDefaultBrowseState() {
    return {
      currentFilter: null,
      sortMethod: "alphabetical",
      navigationMode: "filter_selection",
      searchQuery: "",
      lastUpdated: /* @__PURE__ */ new Date()
    };
  }
}
class NavigationService {
  async generateNavigationSections(sequences, favorites) {
    const sections = [
      await this.generateFavoritesSection(sequences, favorites),
      await this.generateDateSection(sequences),
      await this.generateLengthSection(sequences),
      await this.generateLetterSection(sequences),
      await this.generateLevelSection(sequences),
      await this.generateAuthorSection(sequences)
    ];
    return sections;
  }
  toggleSectionExpansion(sectionId, sections) {
    return sections.map((section) => ({
      ...section,
      isExpanded: section.id === sectionId ? !section.isExpanded : section.isExpanded
    }));
  }
  setActiveItem(sectionId, itemId, sections) {
    return sections.map((section) => ({
      ...section,
      items: section.items.map((item) => ({
        ...item,
        isActive: section.id === sectionId && item.id === itemId
      }))
    }));
  }
  clearActiveStates(sections) {
    return sections.map((section) => ({
      ...section,
      items: section.items.map((item) => ({
        ...item,
        isActive: false
      }))
    }));
  }
  getSequencesForNavigationItem(item, sectionType, allSequences) {
    switch (sectionType) {
      case "length": {
        const length = parseInt(item.value);
        return allSequences.filter((seq) => seq.sequenceLength === length);
      }
      case "letter":
        return allSequences.filter(
          (seq) => seq.word.startsWith(item.value)
        );
      case "level":
        return allSequences.filter((seq) => seq.difficultyLevel === item.value);
      case "author":
        return allSequences.filter((seq) => seq.author === item.value);
      case "date":
        return allSequences.filter((seq) => {
          if (!seq.dateAdded) return false;
          const itemDate = new Date(item.value);
          const seqDate = new Date(seq.dateAdded);
          return seqDate.toDateString() === itemDate.toDateString();
        });
      case "favorites":
        return allSequences;
      default:
        return allSequences;
    }
  }
  updateSectionCounts(sections, sequences, favorites) {
    return sections.map((section) => ({
      ...section,
      totalCount: this.calculateSectionCount(section, sequences, favorites),
      items: section.items.map((item) => ({
        ...item,
        count: this.getSequencesForNavigationItem(item, section.type, sequences).length
      }))
    }));
  }
  // Private helper methods
  async generateFavoritesSection(sequences, favorites) {
    const favoriteSequences = sequences.filter(
      (seq) => favorites.includes(seq.id)
    );
    return {
      id: "favorites",
      title: "⭐ Favorites",
      type: "favorites",
      items: [
        {
          id: "all-favorites",
          label: "All Favorites",
          value: "favorites",
          count: favoriteSequences.length,
          isActive: false
        }
      ],
      isExpanded: false,
      totalCount: favoriteSequences.length
    };
  }
  async generateDateSection(sequences) {
    const dateGroups = /* @__PURE__ */ new Map();
    sequences.forEach((seq) => {
      if (seq.dateAdded) {
        const date = new Date(seq.dateAdded);
        const dateKey = date.toDateString();
        if (!dateGroups.has(dateKey)) {
          dateGroups.set(dateKey, []);
        }
        const group = dateGroups.get(dateKey);
        if (group) {
          group.push(seq);
        }
      }
    });
    const items = Array.from(dateGroups.entries()).sort(([a], [b]) => new Date(b).getTime() - new Date(a).getTime()).slice(0, 10).map(([date, seqs]) => ({
      id: `date-${date}`,
      label: this.formatDateLabel(new Date(date)),
      value: date,
      count: seqs.length,
      isActive: false
    }));
    return {
      id: "date",
      title: "📅 Recently Added",
      type: "date",
      items,
      isExpanded: false,
      totalCount: sequences.filter((seq) => seq.dateAdded).length
    };
  }
  async generateLengthSection(sequences) {
    const lengthGroups = /* @__PURE__ */ new Map();
    sequences.forEach((seq) => {
      const length = seq.sequenceLength || seq.word.length;
      if (!lengthGroups.has(length)) {
        lengthGroups.set(length, []);
      }
      const group = lengthGroups.get(length);
      if (group) {
        group.push(seq);
      }
    });
    const items = Array.from(lengthGroups.entries()).sort(([a], [b]) => a - b).map(([length, seqs]) => ({
      id: `length-${length}`,
      label: `${length} beats`,
      value: length,
      count: seqs.length,
      isActive: false
    }));
    return {
      id: "length",
      title: "📏 Length",
      type: "length",
      items,
      isExpanded: false,
      totalCount: sequences.length
    };
  }
  async generateLetterSection(sequences) {
    const letterGroups = /* @__PURE__ */ new Map();
    sequences.forEach((seq) => {
      const firstLetter = seq.word.charAt(0).toUpperCase();
      if (!letterGroups.has(firstLetter)) {
        letterGroups.set(firstLetter, []);
      }
      const group = letterGroups.get(firstLetter);
      if (group) {
        group.push(seq);
      }
    });
    const items = Array.from(letterGroups.entries()).sort(([a], [b]) => a.localeCompare(b)).map(([letter, seqs]) => ({
      id: `letter-${letter}`,
      label: letter,
      value: letter,
      count: seqs.length,
      isActive: false
    }));
    return {
      id: "letter",
      title: "🔤 Starting Letter",
      type: "letter",
      items,
      isExpanded: true,
      // Default expanded like desktop
      totalCount: sequences.length
    };
  }
  async generateLevelSection(sequences) {
    const levelGroups = /* @__PURE__ */ new Map();
    sequences.forEach((seq) => {
      const level = seq.difficultyLevel || "unknown";
      if (!levelGroups.has(level)) {
        levelGroups.set(level, []);
      }
      const group = levelGroups.get(level);
      if (group) {
        group.push(seq);
      }
    });
    const levelOrder = ["beginner", "intermediate", "advanced", "unknown"];
    const items = levelOrder.filter((level) => levelGroups.has(level)).map((level) => ({
      id: `level-${level}`,
      label: level.charAt(0).toUpperCase() + level.slice(1),
      value: level,
      count: levelGroups.get(level)?.length || 0,
      isActive: false
    }));
    return {
      id: "level",
      title: "📊 Difficulty",
      type: "level",
      items,
      isExpanded: false,
      totalCount: sequences.length
    };
  }
  async generateAuthorSection(sequences) {
    const authorGroups = /* @__PURE__ */ new Map();
    sequences.forEach((seq) => {
      const author = seq.author || "Unknown";
      if (!authorGroups.has(author)) {
        authorGroups.set(author, []);
      }
      const group = authorGroups.get(author);
      if (group) {
        group.push(seq);
      }
    });
    const items = Array.from(authorGroups.entries()).sort(([a], [b]) => a.localeCompare(b)).map(([author, seqs]) => ({
      id: `author-${author}`,
      label: author,
      value: author,
      count: seqs.length,
      isActive: false
    }));
    return {
      id: "author",
      title: "👤 Author",
      type: "author",
      items,
      isExpanded: false,
      totalCount: sequences.length
    };
  }
  calculateSectionCount(section, sequences, favorites) {
    switch (section.type) {
      case "favorites":
        return sequences.filter((seq) => favorites.includes(seq.id)).length;
      default:
        return sequences.length;
    }
  }
  formatDateLabel(date) {
    const now = /* @__PURE__ */ new Date();
    const diffTime = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffTime / (1e3 * 60 * 60 * 24));
    if (diffDays === 0) return "Today";
    if (diffDays === 1) return "Yesterday";
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    return date.toLocaleDateString();
  }
}
class SectionService {
  async organizeSections(sequences, config) {
    if (config.groupBy === "none") {
      return [
        {
          id: "all",
          title: "All Sequences",
          count: sequences.length,
          sequences,
          isExpanded: true,
          sortOrder: 0
        }
      ];
    }
    const grouped = this.groupSequences(sequences, config.groupBy);
    const sections = this.createSections(grouped, config);
    return this.sortSections(sections, config.groupBy);
  }
  toggleSectionExpansion(sectionId, sections) {
    return sections.map((section) => ({
      ...section,
      isExpanded: section.id === sectionId ? !section.isExpanded : section.isExpanded
    }));
  }
  getDefaultSectionConfiguration() {
    return {
      groupBy: "letter",
      sortMethod: "alphabetical",
      showEmptySections: false,
      expandedSections: /* @__PURE__ */ new Set(["A", "B", "C"])
      // Default expand first few sections
    };
  }
  updateSectionConfiguration(config, updates) {
    return {
      ...config,
      ...updates
    };
  }
  getSectionStatistics(sections) {
    const totalSections = sections.length;
    const totalSequences = sections.reduce(
      (sum, section) => sum + section.count,
      0
    );
    const expandedSections = sections.filter(
      (section) => section.isExpanded
    ).length;
    const averageSequencesPerSection = totalSections > 0 ? totalSequences / totalSections : 0;
    return {
      totalSections,
      totalSequences,
      expandedSections,
      averageSequencesPerSection: Math.round(averageSequencesPerSection * 10) / 10
    };
  }
  // Private helper methods
  groupSequences(sequences, groupBy) {
    const groups = /* @__PURE__ */ new Map();
    sequences.forEach((sequence) => {
      const key = this.getGroupKey(sequence, groupBy);
      if (!groups.has(key)) {
        groups.set(key, []);
      }
      groups.get(key).push(sequence);
    });
    return groups;
  }
  getGroupKey(sequence, groupBy) {
    switch (groupBy) {
      case "letter":
        return sequence.word.charAt(0).toUpperCase();
      case "length": {
        const length = sequence.sequenceLength || sequence.word.length;
        return `${length} beats`;
      }
      case "difficulty":
        return sequence.difficultyLevel || "Unknown";
      case "author":
        return sequence.author || "Unknown Author";
      case "date": {
        if (!sequence.dateAdded) return "Unknown Date";
        const date = new Date(sequence.dateAdded);
        return date.toDateString();
      }
      default:
        return "All";
    }
  }
  createSections(grouped, config) {
    const sections = [];
    grouped.forEach((sequences, key) => {
      if (!config.showEmptySections && sequences.length === 0) {
        return;
      }
      const section = {
        id: this.createSectionId(key, config.groupBy),
        title: this.createSectionTitle(key, config.groupBy, sequences.length),
        count: sequences.length,
        sequences: this.sortSequencesInSection(sequences, config.sortMethod),
        isExpanded: config.expandedSections.has(key),
        sortOrder: this.getSectionSortOrder(key, config.groupBy)
      };
      sections.push(section);
    });
    return sections;
  }
  createSectionId(key, groupBy) {
    return `${groupBy}-${key.toLowerCase().replace(/\s+/g, "-")}`;
  }
  createSectionTitle(key, groupBy, count) {
    const countText = count === 1 ? "1 sequence" : `${count} sequences`;
    switch (groupBy) {
      case "letter":
        return `${key} (${countText})`;
      case "length":
        return `${key} (${countText})`;
      case "difficulty": {
        const difficultyEmoji = {
          beginner: "🟢",
          intermediate: "🟡",
          advanced: "🔴",
          Unknown: "⚪"
        }[key] || "⚪";
        return `${difficultyEmoji} ${key} (${countText})`;
      }
      case "author":
        return `👤 ${key} (${countText})`;
      case "date":
        return `📅 ${this.formatDateForSection(key)} (${countText})`;
      default:
        return `${key} (${countText})`;
    }
  }
  sortSequencesInSection(sequences, sortMethod) {
    const sorted = [...sequences];
    switch (sortMethod) {
      case "alphabetical":
        return sorted.sort((a, b) => a.word.localeCompare(b.word));
      case "difficulty_level":
        return sorted.sort((a, b) => {
          const getDifficultyOrder = (level) => {
            switch (level) {
              case "beginner":
                return 1;
              case "intermediate":
                return 2;
              case "advanced":
                return 3;
              default:
                return 0;
            }
          };
          return getDifficultyOrder(a.difficultyLevel) - getDifficultyOrder(b.difficultyLevel);
        });
      case "sequence_length":
        return sorted.sort((a, b) => {
          const lengthA = a.sequenceLength || a.word.length;
          const lengthB = b.sequenceLength || b.word.length;
          return lengthA - lengthB;
        });
      case "date_added":
        return sorted.sort((a, b) => {
          const dateA = a.dateAdded ? new Date(a.dateAdded).getTime() : 0;
          const dateB = b.dateAdded ? new Date(b.dateAdded).getTime() : 0;
          return dateB - dateA;
        });
      case "author":
        return sorted.sort(
          (a, b) => (a.author || "").localeCompare(b.author || "")
        );
      default:
        return sorted;
    }
  }
  sortSections(sections, _groupBy) {
    return sections.sort((a, b) => {
      if (a.sortOrder !== b.sortOrder) {
        return a.sortOrder - b.sortOrder;
      }
      return a.title.localeCompare(b.title);
    });
  }
  getSectionSortOrder(key, groupBy) {
    switch (groupBy) {
      case "letter":
        return key.charCodeAt(0);
      case "length": {
        const match = key.match(/^(\d+)/);
        return match && match[1] ? parseInt(match[1]) : 999;
      }
      case "difficulty": {
        const difficultyOrder = {
          beginner: 1,
          intermediate: 2,
          advanced: 3,
          Unknown: 4
        };
        return difficultyOrder[key] || 999;
      }
      case "author":
        return 0;
      // Will be sorted by title comparison
      case "date": {
        const date = new Date(key);
        return -date.getTime();
      }
      default:
        return 0;
    }
  }
  formatDateForSection(dateString) {
    const date = new Date(dateString);
    const now = /* @__PURE__ */ new Date();
    const diffTime = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffTime / (1e3 * 60 * 60 * 24));
    if (diffDays === 0) return "Today";
    if (diffDays === 1) return "Yesterday";
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    return date.toLocaleDateString();
  }
}
class SequenceIndexService {
  sequenceIndex = null;
  searchIndex = null;
  sequenceMap = /* @__PURE__ */ new Map();
  async loadSequenceIndex() {
    if (this.sequenceIndex !== null) {
      return this.sequenceIndex;
    }
    try {
      if (this.sequenceIndex === null) {
        this.sequenceIndex = await this.scanSequenceDirectory();
      }
      if (this.sequenceIndex) {
        await this.buildSearchIndex(this.sequenceIndex);
      }
      return this.sequenceIndex || [];
    } catch (error) {
      console.error("Failed to load sequence index:", error);
      this.sequenceIndex = [];
      return [];
    }
  }
  async buildSearchIndex(sequences) {
    this.searchIndex = {
      wordIndex: /* @__PURE__ */ new Map(),
      authorIndex: /* @__PURE__ */ new Map(),
      tagIndex: /* @__PURE__ */ new Map(),
      metadataIndex: /* @__PURE__ */ new Map()
    };
    this.sequenceMap.clear();
    for (const sequence of sequences) {
      this.sequenceMap.set(sequence.id, sequence);
      this.addToIndex(
        this.searchIndex.wordIndex,
        sequence.word.toLowerCase(),
        sequence.id
      );
      this.addToIndex(
        this.searchIndex.wordIndex,
        sequence.name.toLowerCase(),
        sequence.id
      );
      if (sequence.author) {
        this.addToIndex(
          this.searchIndex.authorIndex,
          sequence.author.toLowerCase(),
          sequence.id
        );
      }
      for (const tag of sequence.tags) {
        this.addToIndex(
          this.searchIndex.tagIndex,
          tag.toLowerCase(),
          sequence.id
        );
      }
      const searchableText = this.buildSearchableText(sequence);
      for (const term of searchableText.split(/\s+/)) {
        if (term.length > 2) {
          this.addToIndex(
            this.searchIndex.metadataIndex,
            term.toLowerCase(),
            sequence.id
          );
        }
      }
    }
  }
  async searchSequences(query) {
    if (!this.searchIndex || !query.trim()) {
      return this.sequenceIndex || [];
    }
    const searchTerms = query.toLowerCase().split(/\s+/).filter((term) => term.length > 0);
    const resultIds = /* @__PURE__ */ new Set();
    for (const term of searchTerms) {
      const matchingIds = this.searchTerm(term);
      if (resultIds.size === 0) {
        matchingIds.forEach((id) => resultIds.add(id));
      } else {
        const currentIds = new Set(resultIds);
        resultIds.clear();
        matchingIds.forEach((id) => {
          if (currentIds.has(id)) {
            resultIds.add(id);
          }
        });
      }
    }
    const results = Array.from(resultIds).map((id) => this.sequenceMap.get(id)).filter((seq) => seq !== void 0);
    return this.sortByRelevance(results, query);
  }
  async refreshIndex() {
    this.sequenceIndex = null;
    this.searchIndex = null;
    this.sequenceMap.clear();
    await this.loadSequenceIndex();
  }
  // Additional utility methods
  getIndexStats() {
    return {
      totalSequences: this.sequenceMap.size,
      indexedWords: this.searchIndex?.wordIndex.size || 0,
      indexedAuthors: this.searchIndex?.authorIndex.size || 0,
      indexedTags: this.searchIndex?.tagIndex.size || 0,
      indexedMetadata: this.searchIndex?.metadataIndex.size || 0
    };
  }
  async getSequenceById(id) {
    if (!this.sequenceMap.has(id)) {
      await this.loadSequenceIndex();
    }
    return this.sequenceMap.get(id) || null;
  }
  async getSuggestions(partialQuery, maxSuggestions = 10) {
    if (!this.searchIndex || partialQuery.length < 2) {
      return [];
    }
    const suggestions = /* @__PURE__ */ new Set();
    const query = partialQuery.toLowerCase();
    for (const [word] of this.searchIndex.wordIndex) {
      if (word.includes(query)) {
        suggestions.add(word);
        if (suggestions.size >= maxSuggestions) break;
      }
    }
    if (suggestions.size < maxSuggestions) {
      for (const [author] of this.searchIndex.authorIndex) {
        if (author.includes(query)) {
          suggestions.add(author);
          if (suggestions.size >= maxSuggestions) break;
        }
      }
    }
    return Array.from(suggestions).slice(0, maxSuggestions);
  }
  // Private helper methods
  addToIndex(index, key, sequenceId) {
    if (!index.has(key)) {
      index.set(key, /* @__PURE__ */ new Set());
    }
    const keySet = index.get(key);
    if (keySet) {
      keySet.add(sequenceId);
    }
  }
  searchTerm(term) {
    const results = /* @__PURE__ */ new Set();
    if (!this.searchIndex) return results;
    const wordMatches = this.searchIndex.wordIndex.get(term) || /* @__PURE__ */ new Set();
    wordMatches.forEach((id) => results.add(id));
    for (const [word, ids] of this.searchIndex.wordIndex) {
      if (word.includes(term)) {
        ids.forEach((id) => results.add(id));
      }
    }
    const authorMatches = this.searchIndex.authorIndex.get(term) || /* @__PURE__ */ new Set();
    authorMatches.forEach((id) => results.add(id));
    const tagMatches = this.searchIndex.tagIndex.get(term) || /* @__PURE__ */ new Set();
    tagMatches.forEach((id) => results.add(id));
    const metadataMatches = this.searchIndex.metadataIndex.get(term) || /* @__PURE__ */ new Set();
    metadataMatches.forEach((id) => results.add(id));
    return results;
  }
  buildSearchableText(sequence) {
    const parts = [
      sequence.word,
      sequence.name,
      sequence.author || "",
      sequence.difficultyLevel || "",
      sequence.gridMode || "",
      sequence.propType || "",
      ...sequence.tags
    ];
    return parts.filter(Boolean).join(" ");
  }
  sortByRelevance(sequences, query) {
    const queryLower = query.toLowerCase();
    return sequences.sort((a, b) => {
      const scoreA = this.calculateRelevanceScore(a, queryLower);
      const scoreB = this.calculateRelevanceScore(b, queryLower);
      return scoreB - scoreA;
    });
  }
  calculateRelevanceScore(sequence, query) {
    let score = 0;
    if (sequence.word.toLowerCase() === query) {
      score += 100;
    }
    if (sequence.word.toLowerCase().startsWith(query)) {
      score += 50;
    }
    if (sequence.word.toLowerCase().includes(query)) {
      score += 25;
    }
    if (sequence.name.toLowerCase().includes(query)) {
      score += 15;
    }
    if (sequence.author?.toLowerCase().includes(query)) {
      score += 10;
    }
    for (const tag of sequence.tags) {
      if (tag.toLowerCase().includes(query)) {
        score += 5;
      }
    }
    if (sequence.isFavorite) {
      score += 2;
    }
    return score;
  }
  async scanSequenceDirectory() {
    console.warn("Scanning directory - using fallback sample data");
    const sequences = [];
    const knownSequences = [
      "A",
      "AABB",
      "AAKE",
      "AB",
      "ABC",
      "AJEΦ-",
      "AKE",
      "AKIΦ",
      "ALFALGGF",
      "B",
      "BA",
      "BBKE",
      "BBLF",
      "BC",
      "BJEA",
      "BJFA",
      "BKEΦ-",
      "C",
      "CAKE",
      "CCCΦ-",
      "CCKE",
      "CCKΦ"
      // Add more as needed...
    ];
    for (let i = 0; i < knownSequences.length; i++) {
      const word = knownSequences[i];
      if (!word) continue;
      const authors = ["TKA User", "Demo Author", "Expert User"];
      const gridModes = ["diamond", "box"];
      const difficulties = ["beginner", "intermediate", "advanced"];
      const author = authors[i % authors.length];
      const gridMode = gridModes[i % gridModes.length];
      const difficulty = difficulties[i % difficulties.length];
      const result = {
        id: word.toLowerCase().replace(/[^a-z0-9]/g, "_"),
        name: `${word} Sequence`,
        word,
        thumbnails: [`${word}_ver1.png`],
        isFavorite: Math.random() > 0.8,
        isCircular: false,
        tags: ["flow", "practice", "generated"].slice(
          0,
          Math.floor(Math.random() * 3) + 1
        ),
        metadata: { scanned: true, index: i }
      };
      if (author) result.author = author;
      if (gridMode) result.gridMode = gridMode;
      if (difficulty) result.difficultyLevel = difficulty;
      result.sequenceLength = Math.floor(Math.random() * 8) + 3;
      result.level = Math.floor(Math.random() * 4) + 1;
      result.dateAdded = new Date(
        Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1e3
      );
      result.propType = "fans";
      result.startingPosition = "center";
      sequences.push(result);
    }
    return sequences;
  }
}
class ThumbnailService {
  thumbnailCache = /* @__PURE__ */ new Map();
  metadataCache = /* @__PURE__ */ new Map();
  baseUrl = "/dictionary";
  getThumbnailUrl(_sequenceId, thumbnailPath) {
    if (thumbnailPath.startsWith("/dictionary/")) {
      return thumbnailPath;
    }
    if (thumbnailPath.startsWith("/")) {
      return thumbnailPath;
    }
    if (!thumbnailPath.includes("/")) {
      return `${this.baseUrl}/${thumbnailPath}`;
    }
    return `${this.baseUrl}/${thumbnailPath}`;
  }
  async preloadThumbnail(sequenceId, thumbnailPath) {
    const cacheKey = `${sequenceId}-${thumbnailPath}`;
    if (this.thumbnailCache.has(cacheKey)) {
      return this.thumbnailCache.get(cacheKey);
    }
    const preloadPromise = this.loadThumbnailImage(sequenceId, thumbnailPath);
    this.thumbnailCache.set(cacheKey, preloadPromise);
    try {
      await preloadPromise;
    } catch (error) {
      this.thumbnailCache.delete(cacheKey);
      throw error;
    }
  }
  async getThumbnailMetadata(sequenceId) {
    const cacheKey = sequenceId;
    if (this.metadataCache.has(cacheKey)) {
      return this.metadataCache.get(cacheKey) || null;
    }
    try {
      const thumbnailPath = await this.getThumbnailPathForSequence(sequenceId);
      if (!thumbnailPath) {
        return null;
      }
      const metadata = await this.loadImageMetadata(thumbnailPath);
      this.metadataCache.set(cacheKey, metadata);
      return metadata;
    } catch (error) {
      console.warn(
        `Failed to get thumbnail metadata for ${sequenceId}:`,
        error
      );
      return null;
    }
  }
  clearThumbnailCache() {
    this.thumbnailCache.clear();
    this.metadataCache.clear();
  }
  // Additional helper methods for thumbnail management
  async validateThumbnailExists(sequenceId, thumbnailPath) {
    try {
      const url = this.getThumbnailUrl(sequenceId, thumbnailPath);
      const response = await fetch(url, { method: "HEAD" });
      return response.ok;
    } catch {
      return false;
    }
  }
  async getThumbnailsForSequence(sequenceId) {
    const commonPatterns = [
      `${sequenceId}_ver1.png`,
      `${sequenceId.toUpperCase()}_ver1.png`,
      `${sequenceId.toLowerCase()}_ver1.png`
    ];
    const validThumbnails = [];
    for (const pattern of commonPatterns) {
      if (await this.validateThumbnailExists(sequenceId, pattern)) {
        validThumbnails.push(pattern);
      }
    }
    return validThumbnails;
  }
  getOptimizedThumbnailUrl(sequenceId, thumbnailPath, targetWidth) {
    const baseUrl = this.getThumbnailUrl(sequenceId, thumbnailPath);
    return baseUrl;
  }
  // Private helper methods
  async loadThumbnailImage(sequenceId, thumbnailPath) {
    return new Promise((resolve2, reject) => {
      const img = new Image();
      const url = this.getThumbnailUrl(sequenceId, thumbnailPath);
      img.onload = () => {
        this.metadataCache.set(sequenceId, {
          width: img.naturalWidth,
          height: img.naturalHeight
        });
        resolve2();
      };
      img.onerror = () => {
        reject(new Error(`Failed to load thumbnail: ${url}`));
      };
      img.src = url;
    });
  }
  async loadImageMetadata(thumbnailPath) {
    return new Promise((resolve2, reject) => {
      const img = new Image();
      img.onload = () => {
        resolve2({
          width: img.naturalWidth,
          height: img.naturalHeight
        });
      };
      img.onerror = () => {
        reject(new Error(`Failed to load image metadata: ${thumbnailPath}`));
      };
      img.src = thumbnailPath;
    });
  }
  async getThumbnailPathForSequence(sequenceId) {
    const patterns = [
      `${sequenceId}_ver1.png`,
      `${sequenceId.toUpperCase()}_ver1.png`,
      `${sequenceId.toLowerCase()}_ver1.png`
    ];
    for (const pattern of patterns) {
      if (await this.validateThumbnailExists(sequenceId, pattern)) {
        return pattern;
      }
    }
    return null;
  }
  // Batch operations for performance
  async preloadThumbnails(thumbnails) {
    const preloadPromises = thumbnails.map(
      (thumb) => this.preloadThumbnail(thumb.sequenceId, thumb.thumbnailPath).catch(
        (error) => {
          console.warn(
            `Failed to preload thumbnail ${thumb.sequenceId}/${thumb.thumbnailPath}:`,
            error
          );
        }
      )
    );
    await Promise.all(preloadPromises);
  }
  getThumbnailCacheStats() {
    return {
      cached: this.thumbnailCache.size,
      metadataCached: this.metadataCache.size
    };
  }
}
const IBrowseServiceInterface = createServiceInterface$1(
  "IBrowseService",
  BrowseService
);
const IThumbnailServiceInterface = createServiceInterface$1(
  "IThumbnailService",
  ThumbnailService
);
const ISequenceIndexServiceInterface = createServiceInterface$1(
  "ISequenceIndexService",
  SequenceIndexService
);
const IFavoritesServiceInterface = createServiceInterface$1(
  "IFavoritesService",
  FavoritesService
);
const INavigationServiceInterface = createServiceInterface$1(
  "INavigationService",
  NavigationService
);
const ISectionServiceInterface = createServiceInterface$1(
  "ISectionService",
  SectionService
);
const IFilterPersistenceServiceInterface = createServiceInterface$1(
  "IFilterPersistenceService",
  FilterPersistenceService
);
const IDeleteServiceInterface = createServiceInterface$1(
  "IDeleteService",
  DeleteService
);
function createServiceInterface(token, implementation) {
  return { token, implementation };
}
class AnimatedPictographDataService {
  /**
   * Creates complete pictograph data for animated display using current motion parameters.
   * Generates proper props, arrows, and motion data for realistic visualization.
   */
  createAnimatedPictographData(motionState) {
    try {
      const gridMode = this.getGridMode(motionState.gridType);
      const gridData = createGridData$1({ grid_mode: gridMode });
      const blueMotionData = this.createCompleteMotionData(
        motionState.blueMotionParams
      );
      const redMotionData = this.createCompleteMotionData(
        motionState.redMotionParams
      );
      const blueProps = this.createPropDataFromMotion(
        motionState.blueMotionParams,
        "blue"
      );
      const redProps = this.createPropDataFromMotion(
        motionState.redMotionParams,
        "red"
      );
      const blueArrows = this.createArrowDataFromMotion(
        motionState.blueMotionParams,
        "blue"
      );
      const redArrows = this.createArrowDataFromMotion(
        motionState.redMotionParams,
        "red"
      );
      const pictographData = createPictographData({
        id: "motion-tester-animated-pictograph",
        grid_data: gridData,
        arrows: {
          blue: blueArrows,
          red: redArrows
        },
        props: {
          blue: blueProps,
          red: redProps
        },
        motions: {
          blue: blueMotionData,
          red: redMotionData
        },
        letter: "T",
        // T for "Tester"
        beat: 1,
        is_blank: false,
        is_mirrored: false,
        metadata: {
          source: "motion_tester_animated",
          grid_type: motionState.gridType,
          progress: motionState.animationState.progress
        }
      });
      return pictographData;
    } catch (error) {
      console.error("Error creating animated pictograph data:", error);
      return null;
    }
  }
  getGridMode(gridType) {
    return gridType === "diamond" ? GridMode.DIAMOND : GridMode.BOX;
  }
  /**
   * Creates complete motion data using the domain factory function
   */
  createCompleteMotionData(motionParams) {
    return createMotionData({
      motion_type: this.mapMotionType(motionParams.motionType),
      start_loc: this.mapLocation(motionParams.startLoc),
      end_loc: this.mapLocation(motionParams.endLoc),
      start_ori: this.mapOrientation(motionParams.startOri),
      end_ori: this.mapOrientation(motionParams.endOri),
      prop_rot_dir: this.mapRotationDirection(motionParams.propRotDir),
      turns: motionParams.turns,
      is_visible: true
    });
  }
  /**
   * Creates prop data based on motion parameters
   */
  createPropDataFromMotion(motionParams, color) {
    return createPropData({
      prop_type: PropType.STAFF,
      // Default to staff for motion tester
      color,
      location: this.mapLocation(motionParams.startLoc),
      orientation: this.mapOrientation(motionParams.startOri),
      rotation_direction: this.mapRotationDirection(motionParams.propRotDir),
      is_visible: true
    });
  }
  /**
   * Creates arrow data based on motion parameters
   */
  createArrowDataFromMotion(motionParams, color) {
    return createArrowData({
      arrow_type: color === "blue" ? ArrowType.BLUE : ArrowType.RED,
      color,
      motion_type: motionParams.motionType,
      start_orientation: motionParams.startOri,
      end_orientation: motionParams.endOri,
      rotation_direction: motionParams.propRotDir,
      turns: motionParams.turns,
      location: this.mapLocation(motionParams.startLoc),
      is_visible: true
    });
  }
  // Mapping methods to convert motion tester parameters to domain enums
  mapMotionType(motionType) {
    if (!motionType) return MotionType.STATIC;
    switch (motionType.toLowerCase()) {
      case "pro":
        return MotionType.PRO;
      case "anti":
        return MotionType.ANTI;
      case "float":
        return MotionType.FLOAT;
      case "dash":
        return MotionType.DASH;
      case "static":
        return MotionType.STATIC;
      default:
        return MotionType.STATIC;
    }
  }
  mapLocation(location) {
    if (!location) return Location.NORTH;
    switch (location.toLowerCase()) {
      case "n":
        return Location.NORTH;
      case "e":
        return Location.EAST;
      case "s":
        return Location.SOUTH;
      case "w":
        return Location.WEST;
      case "ne":
        return Location.NORTHEAST;
      case "se":
        return Location.SOUTHEAST;
      case "sw":
        return Location.SOUTHWEST;
      case "nw":
        return Location.NORTHWEST;
      default:
        return Location.NORTH;
    }
  }
  mapOrientation(orientation) {
    if (!orientation) return Orientation.IN;
    switch (orientation.toLowerCase()) {
      case "in":
        return Orientation.IN;
      case "out":
        return Orientation.OUT;
      case "clock":
        return Orientation.CLOCK;
      case "counter":
        return Orientation.COUNTER;
      default:
        return Orientation.IN;
    }
  }
  mapRotationDirection(rotationDir) {
    if (!rotationDir) return RotationDirection.NO_ROTATION;
    switch (rotationDir.toLowerCase()) {
      case "cw":
      case "clockwise":
        return RotationDirection.CLOCKWISE;
      case "ccw":
      case "counter_clockwise":
        return RotationDirection.COUNTER_CLOCKWISE;
      case "no_rot":
      case "no_rotation":
        return RotationDirection.NO_ROTATION;
      default:
        return RotationDirection.NO_ROTATION;
    }
  }
}
const IAnimatedPictographDataServiceInterface = createServiceInterface(
  "IAnimatedPictographDataService",
  AnimatedPictographDataService
);
const serviceInterfaceMap = /* @__PURE__ */ new Map([
  // Core services
  ["ISequenceService", ISequenceServiceInterface],
  ["ISequenceDomainService", ISequenceDomainServiceInterface],
  ["IPictographService", IPictographServiceInterface],
  ["IPictographRenderingService", IPictographRenderingServiceInterface],
  ["IPropRenderingService", IPropRenderingServiceInterface],
  ["IPersistenceService", IPersistenceServiceInterface],
  ["ISettingsService", ISettingsServiceInterface],
  ["IDeviceDetectionService", IDeviceDetectionServiceInterface],
  [
    "IApplicationInitializationService",
    IApplicationInitializationServiceInterface
  ],
  ["IExportService", IExportServiceInterface],
  ["IMotionGenerationService", IMotionGenerationServiceInterface],
  ["ISequenceGenerationService", ISequenceGenerationServiceInterface],
  [
    "IConstructTabCoordinationService",
    IConstructTabCoordinationServiceInterface
  ],
  ["IOptionDataService", IOptionDataServiceInterface],
  ["IStartPositionService", IStartPositionServiceInterface],
  ["IPanelManagementService", IPanelManagementServiceInterface],
  // Positioning services
  ["IArrowPositioningService", IArrowPositioningServiceInterface],
  ["IArrowPlacementDataService", IArrowPlacementDataServiceInterface],
  ["IArrowPlacementKeyService", IArrowPlacementKeyServiceInterface],
  ["IArrowLocationCalculator", IArrowLocationCalculatorInterface],
  ["IArrowRotationCalculator", IArrowRotationCalculatorInterface],
  ["IArrowAdjustmentCalculator", IArrowAdjustmentCalculatorInterface],
  ["IArrowCoordinateSystemService", IArrowCoordinateSystemServiceInterface],
  ["IDashLocationCalculator", IDashLocationCalculatorInterface],
  ["IDirectionalTupleProcessor", IDirectionalTupleProcessorInterface],
  ["IArrowPositioningOrchestrator", IArrowPositioningOrchestratorInterface],
  ["IPositioningServiceFactory", IPositioningServiceFactoryInterface],
  // Browse services
  ["IBrowseService", IBrowseServiceInterface],
  ["IThumbnailService", IThumbnailServiceInterface],
  ["ISequenceIndexService", ISequenceIndexServiceInterface],
  ["IFavoritesService", IFavoritesServiceInterface],
  ["INavigationService", INavigationServiceInterface],
  ["ISectionService", ISectionServiceInterface],
  ["IFilterPersistenceService", IFilterPersistenceServiceInterface],
  ["IDeleteService", IDeleteServiceInterface],
  // Motion Tester services
  ["IAnimatedPictographDataService", IAnimatedPictographDataServiceInterface]
]);
function getContainer() {
  {
    throw new Error(
      "Application container not initialized. Call createWebApplication() first."
    );
  }
}
function resolve(serviceInterface) {
  const container = getContainer();
  {
    const mappedInterface = serviceInterfaceMap.get(serviceInterface);
    if (!mappedInterface) {
      throw new Error(
        `Service interface not found for key: ${serviceInterface}`
      );
    }
    return container.resolve(mappedInterface);
  }
}
function LoadingScreen($$payload, $$props) {
  let { progress = 0, message = "Loading..." } = $$props;
  const clampedProgress = Math.max(0, Math.min(100, progress));
  $$payload.out.push(`<!---->/** * Loading Screen - Pure Svelte 5 implementation * * Shows loading progress during application
initialization. */ <div class="loading-screen svelte-191ks69"><div class="loading-content svelte-191ks69"><div class="spinner svelte-191ks69"></div> <h2 class="svelte-191ks69">TKA - The Kinetic Constructor</h2> <p class="message svelte-191ks69">${escape_html(message)}</p> <div class="progress-container svelte-191ks69"><div class="progress-bar svelte-191ks69"><div class="progress-fill svelte-191ks69"${attr_style(`width: ${stringify(clampedProgress)}%`)}></div></div> <span class="progress-text svelte-191ks69">${escape_html(Math.round(clampedProgress))}%</span></div></div></div>`);
}
class ArrowPositioningService2 {
  orchestrator;
  constructor() {
    const factory = getPositioningServiceFactory();
    this.orchestrator = factory.createPositioningOrchestrator();
  }
  /**
   * Calculate arrow position using the sophisticated positioning pipeline
   */
  async calculatePosition(arrowData, motionData, pictographData) {
    console.log(
      `🎯 ArrowPositioningService.calculatePosition called for ${arrowData.color} arrow`
    );
    console.log(`Arrow data:`, {
      motion_type: arrowData.motion_type,
      start_orientation: arrowData.start_orientation,
      end_orientation: arrowData.end_orientation,
      turns: arrowData.turns,
      position_x: arrowData.position_x,
      position_y: arrowData.position_y
    });
    console.log(`Motion data:`, {
      motion_type: motionData.motion_type,
      start_loc: motionData.start_loc,
      end_loc: motionData.end_loc,
      turns: motionData.turns
    });
    try {
      console.log(`🔧 Calling orchestrator.calculateArrowPosition...`);
      const [x, y, rotation] = this.orchestrator.calculateArrowPosition(
        arrowData,
        pictographData,
        motionData
      );
      console.log(
        `✅ Orchestrator returned: (${x}, ${y}) rotation: ${rotation}°`
      );
      return { x, y, rotation };
    } catch (error) {
      console.error("Sophisticated positioning failed, using fallback:", error);
      return this.getFallbackPosition(motionData);
    }
  }
  /**
   * Synchronous position calculation (may not include full adjustments)
   */
  calculatePositionSync(arrowData, motionData, pictographData) {
    try {
      console.log(`🎯 Calculating sync position for ${arrowData.color} arrow`);
      console.log(
        `Motion: ${motionData.motion_type}, Start: ${motionData.start_loc}, End: ${motionData.end_loc}`
      );
      const [x, y, rotation] = this.orchestrator.calculateArrowPosition(
        arrowData,
        pictographData,
        motionData
      );
      console.log(
        `✅ Calculated sync position: (${x}, ${y}) rotation: ${rotation}°`
      );
      return { x, y, rotation };
    } catch (error) {
      console.error("Synchronous positioning failed, using fallback:", error);
      return this.getFallbackPosition(motionData);
    }
  }
  /**
   * Determine if arrow should be mirrored based on motion data
   */
  shouldMirror(arrowData, _motionData, pictographData) {
    try {
      return this.orchestrator.shouldMirrorArrow(arrowData, pictographData);
    } catch (error) {
      console.warn("Failed to determine mirror state, using default:", error);
      return false;
    }
  }
  /**
   * Legacy interface for backward compatibility
   */
  async calculatePosition_legacy(input) {
    const arrowData = {
      color: input.arrow_type,
      arrow_type: input.arrow_type === "blue" ? ArrowType.BLUE : ArrowType.RED,
      location: input.location,
      motion_type: input.motion_type
    };
    const motionData = {
      motion_type: input.motion_type,
      start_loc: input.location,
      start_ori: input.start_orientation || "in",
      end_ori: input.end_orientation || "in",
      prop_rot_dir: "cw",
      turns: input.turns
    };
    const pictographData = {
      letter: input.letter || "A",
      grid_mode: input.grid_mode,
      motions: {
        [input.arrow_type]: motionData
      }
    };
    const result = await this.calculatePosition(
      arrowData,
      motionData,
      pictographData
    );
    return { x: result.x, y: result.y };
  }
  /**
   * Fallback position calculation using basic coordinates
   */
  getFallbackPosition(motionData) {
    const coordinates = this.calculateLocationCoordinates(
      motionData.start_loc || "center"
    );
    console.log(
      `🔄 Using fallback position: (${coordinates.x}, ${coordinates.y})`
    );
    return {
      x: coordinates.x,
      y: coordinates.y,
      rotation: 0
    };
  }
  /**
   * Basic coordinate calculation as fallback
   */
  calculateLocationCoordinates(location) {
    const diamondCoordinates = {
      // Cardinal directions (hand_points)
      n: { x: 475, y: 331.9 },
      e: { x: 618.1, y: 475 },
      s: { x: 475, y: 618.1 },
      w: { x: 331.9, y: 475 },
      // Diagonal directions (layer2_points) - used for arrows
      ne: { x: 618.1, y: 331.9 },
      se: { x: 618.1, y: 618.1 },
      sw: { x: 331.9, y: 618.1 },
      nw: { x: 331.9, y: 331.9 },
      // Center point
      center: { x: 475, y: 475 }
    };
    const coords = diamondCoordinates[location.toLowerCase()];
    return coords || { x: 475, y: 475 };
  }
}
new ArrowPositioningService2();
class ConstructTabEventService {
  constructCoordinator = null;
  constructor() {
    this.initializeServices();
  }
  initializeServices() {
    try {
      this.constructCoordinator = resolve("IConstructTabCoordinationService");
    } catch {
    }
  }
  /**
   * Handle start position selection in the Build tab
   */
  async handleStartPositionSelected(startPosition) {
    try {
      console.log(
        "🎭 Start position selected in ConstructTabEventService:",
        startPosition.pictograph_data?.id
      );
      if (!this.constructCoordinator) {
        console.log(
          "🎭 Coordination service not available, attempting to resolve..."
        );
        try {
          this.constructCoordinator = resolve(
            "IConstructTabCoordinationService"
          );
          console.log("✅ Coordination service resolved successfully");
        } catch (resolveError) {
          console.error(
            "❌ Failed to resolve coordination service:",
            resolveError
          );
          throw new Error("Coordination service not available");
        }
      }
      if (this.constructCoordinator) {
        console.log(
          "🎭 Calling coordination service handleStartPositionSet..."
        );
        await this.constructCoordinator.handleStartPositionSet(startPosition);
        console.log("✅ Coordination service handleStartPositionSet completed");
      } else {
        throw new Error(
          "Coordination service is null after resolution attempt"
        );
      }
      console.log("✅ Transitioned to option picker");
    } catch (error) {
      console.error("❌ Error handling start position selection:", error);
      throw error;
    }
  }
  /**
   * Handle option selection in the Build tab
   */
  async handleOptionSelected(option) {
    try {
      console.log("🎭 Option selected in ConstructTabEventService:", option.id);
      const beatData = createBeatData({
        beat_number: 1,
        // Default for now - should be passed as parameter
        pictograph_data: option
      });
      if (this.constructCoordinator) {
        await this.constructCoordinator.handleBeatAdded(beatData);
      }
      console.log("✅ Beat added to sequence");
    } catch (error) {
      console.error("❌ Error handling option selection:", error);
      throw error;
    }
  }
  /**
   * Handle beat modification from the Graph Editor
   */
  handleBeatModified(beatIndex, beatData) {
    console.log(
      "ConstructTabEventService: Beat modified in graph editor",
      beatIndex,
      beatData
    );
    console.log("Beat modification handled locally for beat index:", beatIndex);
  }
  /**
   * Handle arrow selection from the Graph Editor
   */
  handleArrowSelected(arrowData) {
    console.log(
      "ConstructTabEventService: Arrow selected in graph editor",
      arrowData
    );
  }
  /**
   * Handle graph editor visibility changes
   */
  handleGraphEditorVisibilityChanged(isVisible) {
    console.log(
      "ConstructTabEventService: Graph editor visibility changed",
      isVisible
    );
  }
  /**
   * Handle export setting changes from the Export Panel
   */
  handleExportSettingChanged(event) {
    const { setting, value } = event.detail;
    console.log(
      "ConstructTabEventService: Export setting changed",
      setting,
      value
    );
  }
  /**
   * Handle preview update requests from the Export Panel
   */
  handlePreviewUpdateRequested(event) {
    const settings = event.detail;
    console.log("ConstructTabEventService: Preview update requested", settings);
  }
  /**
   * Handle export requests from the Export Panel
   */
  handleExportRequested(event) {
    const { type, config } = event.detail;
    console.log("ConstructTabEventService: Export requested", type, config);
    if (type === "current") {
      console.log("Exporting current sequence:", config.sequence?.name);
      alert(
        `Exporting sequence "${config.sequence?.name || "Untitled"}" with ${config.sequence?.beats?.length || 0} beats`
      );
    } else if (type === "all") {
      console.log("Exporting all sequences");
      alert("Exporting all sequences in library");
    }
  }
  /**
   * Setup component coordination
   */
  setupComponentCoordination() {
    console.log("🎭 ConstructTabEventService setting up coordination");
    if (this.constructCoordinator) {
      this.constructCoordinator.setupComponentCoordination({
        constructTab: {
          handleEvent: (eventType, data) => {
            switch (eventType) {
              case "ui_transition":
                break;
              default:
                console.log(
                  `ConstructTabEventService received event: ${eventType}`,
                  data
                );
            }
          }
        }
      });
    }
  }
}
new ConstructTabEventService();
typeof window !== "undefined" && window.location.search.includes("debug=foldable");
function MainApplication($$payload, $$props) {
  push();
  getContext("di-container");
  let initializationProgress = getInitializationProgress();
  head($$payload, ($$payload2) => {
    $$payload2.title = `<title>TKA Constructor - The Kinetic Alphabet</title>`;
    $$payload2.out.push(`<meta name="description" content="The Kinetic Alphabet is a revolutionary flow arts choreography toolbox for poi, staff, fans, and other flow arts. Create, learn, and share movement sequences."/>`);
  });
  $$payload.out.push(`<div class="tka-app svelte-e0pyof" data-testid="tka-application">`);
  {
    $$payload.out.push("<!--[!-->");
    {
      $$payload.out.push("<!--[-->");
      LoadingScreen($$payload, {
        progress: initializationProgress,
        message: "Initializing Constructor..."
      });
    }
    $$payload.out.push(`<!--]-->`);
  }
  $$payload.out.push(`<!--]--></div>`);
  pop();
}
export {
  MainApplication as M
};
