import type { ButtonDefinition, ActionEventDetail } from './types';
import { sequenceActions, sequenceSelectors } from '$lib/state/machines/sequenceMachine';
import hapticFeedbackService from '$lib/services/HapticFeedbackService';

/**
 * Defines the button panel buttons used in the sequence widget
 */
export function getButtonPanelButtons(): ButtonDefinition[] {
    return [
        // Mode switching tools
        {
            icon: 'fa-hammer',
            title: 'Construct',
            id: 'constructMode',
            color: '#4361ee'
        },
        {
            icon: 'fa-robot',
            title: 'Generate',
            id: 'generateMode',
            color: '#3a86ff'
        },
        // Sharing and viewing tools
        { icon: 'fa-share-nodes', title: 'Share', id: 'saveImage', color: '#3a86ff' },
        { icon: 'fa-expand', title: 'Full Screen', id: 'viewFullScreen', color: '#4cc9f0' },
        // Sequence manipulation tools
        {
            icon: 'fa-arrows-left-right',
            title: 'Mirror',
            id: 'mirrorSequence',
            color: '#4895ef'
        },
        { icon: 'fa-paintbrush', title: 'Swap Colors', id: 'swapColors', color: '#ff6b6b' },
        { icon: 'fa-rotate', title: 'Rotate', id: 'rotateSequence', color: '#f72585' },
        // Dictionary tool
        {
            icon: 'fa-book-medical',
            title: 'Add to Dictionary',
            id: 'addToDictionary',
            color: '#4361ee'
        },
        // Destructive actions
        { icon: 'fa-trash', title: 'Delete Beat', id: 'deleteBeat', color: '#ff9e00' }
    ];
}

export interface ButtonActionHandlerParams {
    id: string;
    activeMode: 'construct' | 'generate';
    setActiveMode: (mode: 'construct' | 'generate') => void;
    closeToolsPanel?: () => void;
    openFullScreen?: () => void;
}

export function handleButtonAction(params: ButtonActionHandlerParams): void {
    const { id, activeMode, setActiveMode, closeToolsPanel, openFullScreen } = params;

    switch (id) {
        case 'constructMode':
            hapticFeedbackService.trigger('navigation');
            setActiveMode('construct');
            const constructEvent = new CustomEvent('switch-mode', {
                detail: { mode: 'construct' },
                bubbles: true
            });
            document.dispatchEvent(constructEvent);
            break;
        case 'generateMode':
            hapticFeedbackService.trigger('navigation');
            setActiveMode('generate');
            const generateEvent = new CustomEvent('switch-mode', {
                detail: { mode: 'generate' },
                bubbles: true
            });
            document.dispatchEvent(generateEvent);
            break;
        case 'addToDictionary':
            hapticFeedbackService.trigger('success');
            // Handle add to dictionary action
            break;
        case 'saveImage':
            hapticFeedbackService.trigger('success');
            // Handle save image action
            break;
        case 'viewFullScreen':
            hapticFeedbackService.trigger('navigation');
            if (openFullScreen) {
                openFullScreen();
            }
            break;
        case 'mirrorSequence':
            hapticFeedbackService.trigger('selection');
            // Handle mirror sequence action
            break;
        case 'swapColors':
            hapticFeedbackService.trigger('selection');
            // Handle swap colors action
            break;
        case 'rotateSequence':
            hapticFeedbackService.trigger('selection');
            // Handle rotate sequence action
            break;
        case 'deleteBeat':
            hapticFeedbackService.trigger('warning');
            const selectedBeatIds = sequenceSelectors.selectedBeatIds();
            if (selectedBeatIds.length > 0) {
                sequenceActions.removeBeatAndFollowing(selectedBeatIds[0]);
            }
            break;
        case 'clearSequence':
            hapticFeedbackService.trigger('error');
            sequenceActions.clearSequence();
            break;
    }

    if (closeToolsPanel) {
        closeToolsPanel();
    }
}
