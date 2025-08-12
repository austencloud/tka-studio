/**
 * ✅ TKA VALIDATION ENGINE
 * 
 * Comprehensive validation system for service registration and resolution
 * with detailed error reporting and suggestions.
 */

import { 
    ServiceInterface, 
    ValidationResult, 
    ValidationError, 
    ValidationWarning,
    ServiceFactory,
    Constructor
} from './types.js';

export class ValidationEngine {
    private readonly _validationRules: ValidationRule[] = [];
    private _strictMode = true;

    constructor() {
        this._registerDefaultRules();
    }

    /**
     * Validate service registration
     */
    validateRegistration<T>(
        serviceInterface: ServiceInterface<T>, 
        implementation: Constructor<T>
    ): ValidationResult {
        const errors: ValidationError[] = [];
        const warnings: ValidationWarning[] = [];

        // Run all validation rules
        for (const rule of this._validationRules) {
            try {
                const result = rule.validate(serviceInterface, implementation);
                errors.push(...result.errors);
                warnings.push(...result.warnings);
            } catch (error) {
                errors.push({
                    code: 'VALIDATION_RULE_ERROR',
                    message: `Validation rule '${rule.name}' failed: ${error}`,
                    severity: 'error',
                    context: { rule: rule.name, error }
                });
            }
        }

        const isValid = errors.length === 0 || (!this._strictMode && errors.every(e => e.severity !== 'error'));

        if (!isValid && this._strictMode) {
            throw new Error(`Service registration validation failed for '${serviceInterface.name}': ${errors.map(e => e.message).join(', ')}`);
        }

        return { isValid, errors, warnings };
    }

    /**
     * Validate factory registration
     */
    validateFactoryRegistration<T>(
        serviceInterface: ServiceInterface<T>, 
        factory: ServiceFactory<T>
    ): ValidationResult {
        const errors: ValidationError[] = [];
        const warnings: ValidationWarning[] = [];

        // Basic factory validation
        if (!factory || typeof factory !== 'function') {
            errors.push({
                code: 'INVALID_FACTORY',
                message: 'Factory must be a function',
                severity: 'error',
                context: { serviceInterface: serviceInterface.name, factory }
            });
        }

        // Check factory signature
        if (factory && factory.length > 1) {
            warnings.push({
                code: 'FACTORY_MULTIPLE_PARAMETERS',
                message: 'Factory function has multiple parameters, only container will be passed',
                suggestion: 'Consider using a factory that accepts only the container parameter',
                context: { serviceInterface: serviceInterface.name, parameterCount: factory.length }
            });
        }

        const isValid = errors.length === 0;
        return { isValid, errors, warnings };
    }

    /**
     * Validate instance registration
     */
    validateInstanceRegistration<T>(
        serviceInterface: ServiceInterface<T>, 
        instance: T
    ): ValidationResult {
        const errors: ValidationError[] = [];
        const warnings: ValidationWarning[] = [];

        // Basic instance validation
        if (instance === null || instance === undefined) {
            errors.push({
                code: 'NULL_INSTANCE',
                message: 'Instance cannot be null or undefined',
                severity: 'error',
                context: { serviceInterface: serviceInterface.name }
            });
        }

        // Type compatibility check (basic)
        if (instance && serviceInterface.type) {
            try {
                // Check if instance has expected methods/properties
                const expectedPrototype = serviceInterface.type.prototype;
                if (expectedPrototype) {
                    const missingMethods = this._findMissingMethods(instance, expectedPrototype);
                    if (missingMethods.length > 0) {
                        warnings.push({
                            code: 'MISSING_METHODS',
                            message: `Instance may not fully implement interface: missing ${missingMethods.join(', ')}`,
                            suggestion: 'Ensure instance implements all interface methods',
                            context: { serviceInterface: serviceInterface.name, missingMethods }
                        });
                    }
                }
            } catch (error) {
                // Type checking failed, but continue
                warnings.push({
                    code: 'TYPE_CHECK_FAILED',
                    message: 'Could not verify type compatibility',
                    context: { serviceInterface: serviceInterface.name, error }
                });
            }
        }

        const isValid = errors.length === 0;
        return { isValid, errors, warnings };
    }

    /**
     * Set strict mode for validation
     */
    setStrictMode(strict: boolean): void {
        this._strictMode = strict;
    }

    /**
     * Add custom validation rule
     */
    addValidationRule(rule: ValidationRule): void {
        this._validationRules.push(rule);
    }

    /**
     * Remove validation rule by name
     */
    removeValidationRule(name: string): boolean {
        const index = this._validationRules.findIndex(r => r.name === name);
        if (index >= 0) {
            this._validationRules.splice(index, 1);
            return true;
        }
        return false;
    }

    /**
     * Get all validation rules
     */
    getValidationRules(): ValidationRule[] {
        return [...this._validationRules];
    }

    private _registerDefaultRules(): void {
        // Interface name validation
        this.addValidationRule({
            name: 'InterfaceNameValidation',
            validate: (serviceInterface, implementation) => {
                const errors: ValidationError[] = [];
                const warnings: ValidationWarning[] = [];

                if (!serviceInterface.name || serviceInterface.name.trim() === '') {
                    errors.push({
                        code: 'EMPTY_INTERFACE_NAME',
                        message: 'Service interface name cannot be empty',
                        severity: 'error'
                    });
                }

                if (serviceInterface.name && !serviceInterface.name.startsWith('I')) {
                    warnings.push({
                        code: 'INTERFACE_NAMING_CONVENTION',
                        message: 'Interface names should start with "I" by convention',
                        suggestion: `Consider renaming to "I${serviceInterface.name}"`
                    });
                }

                return { isValid: errors.length === 0, errors, warnings };
            }
        });

        // Implementation validation
        this.addValidationRule({
            name: 'ImplementationValidation',
            validate: (serviceInterface, implementation) => {
                const errors: ValidationError[] = [];
                const warnings: ValidationWarning[] = [];

                if (!implementation) {
                    errors.push({
                        code: 'MISSING_IMPLEMENTATION',
                        message: 'Implementation is required',
                        severity: 'error'
                    });
                    return { isValid: false, errors, warnings };
                }

                if (typeof implementation !== 'function') {
                    errors.push({
                        code: 'INVALID_IMPLEMENTATION',
                        message: 'Implementation must be a constructor function',
                        severity: 'error'
                    });
                }

                // Check if implementation is instantiable
                try {
                    new implementation();
                } catch (error) {
                    warnings.push({
                        code: 'IMPLEMENTATION_NOT_INSTANTIABLE',
                        message: 'Implementation may not be instantiable with default constructor',
                        suggestion: 'Ensure implementation has a valid constructor',
                        context: { error }
                    });
                }

                return { isValid: errors.length === 0, errors, warnings };
            }
        });

        // Circular dependency detection (basic)
        this.addValidationRule({
            name: 'CircularDependencyDetection',
            validate: (serviceInterface, implementation) => {
                const errors: ValidationError[] = [];
                const warnings: ValidationWarning[] = [];

                // This would be more sophisticated in a real implementation
                // For now, just check if service depends on itself
                if (implementation && implementation.name === serviceInterface.name.substring(1)) {
                    warnings.push({
                        code: 'POTENTIAL_CIRCULAR_DEPENDENCY',
                        message: 'Service may have circular dependency with itself',
                        suggestion: 'Review service dependencies to avoid circular references'
                    });
                }

                return { isValid: true, errors, warnings };
            }
        });

        // Deprecated service warning
        this.addValidationRule({
            name: 'DeprecatedServiceWarning',
            validate: (serviceInterface, implementation) => {
                const errors: ValidationError[] = [];
                const warnings: ValidationWarning[] = [];

                if (serviceInterface.metadata?.deprecated) {
                    warnings.push({
                        code: 'DEPRECATED_SERVICE',
                        message: serviceInterface.metadata.deprecationMessage || 'Service is deprecated',
                        suggestion: 'Consider using an alternative service'
                    });
                }

                return { isValid: true, errors, warnings };
            }
        });
    }

    private _findMissingMethods(instance: any, prototype: any): string[] {
        const missing: string[] = [];
        
        if (!prototype) return missing;

        const prototypeProps = Object.getOwnPropertyNames(prototype);
        for (const prop of prototypeProps) {
            if (prop !== 'constructor' && typeof prototype[prop] === 'function') {
                if (!instance[prop] || typeof instance[prop] !== 'function') {
                    missing.push(prop);
                }
            }
        }

        return missing;
    }
}

/**
 * Interface for custom validation rules
 */
export interface ValidationRule {
    readonly name: string;
    validate(serviceInterface: ServiceInterface, implementation?: Constructor<any>): ValidationResult;
}
