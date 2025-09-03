// src/lib/state/stores/learn/progressStore.ts
import { writable, derived, get } from 'svelte/store';
import { browser } from '$app/environment';

// Define types for progress tracking
export interface LessonProgress {
    completed: number;
    total: number;
    lastScore: number;
    lastCompletedDate?: string;
    attempts: number;
}

export interface ProgressState {
    lessonProgress: Record<string, LessonProgress>;
    totalQuestionsAnswered: number;
    totalLessonsStarted: number;
    totalLessonsCompleted: number;
    averageScore: number;
}

// Initial state
const initialState: ProgressState = {
    lessonProgress: {
        letter_to_pictograph: { completed: 12, total: 30, lastScore: 85, attempts: 3 },
        pictograph_to_letter: { completed: 8, total: 30, lastScore: 70, attempts: 2 },
        turns: { completed: 0, total: 30, lastScore: 0, attempts: 0 },
        positions: { completed: 0, total: 30, lastScore: 0, attempts: 0 }
    },
    totalQuestionsAnswered: 20,
    totalLessonsStarted: 2,
    totalLessonsCompleted: 0,
    averageScore: 78
};

// Load progress from localStorage if available
function loadProgress(): ProgressState {
    if (browser) {
        const savedProgress = localStorage.getItem('learnProgress');
        if (savedProgress) {
            try {
                return JSON.parse(savedProgress);
            } catch (e) {
                console.error('Failed to parse saved progress:', e);
            }
        }
    }
    return initialState;
}

// Create the store
function createProgressStore() {
    const { subscribe, set, update } = writable<ProgressState>(loadProgress());

    // Save to localStorage when updated
    subscribe((state) => {
        if (browser) {
            localStorage.setItem('learnProgress', JSON.stringify(state));
        }
    });

    return {
        subscribe,

        // Update progress for a specific lesson
        updateLessonProgress: (
            lessonId: string,
            score: number,
            questionsCompleted: number,
            totalQuestions: number
        ) => {
            update((state) => {
                // Get current progress for this lesson
                const currentProgress = state.lessonProgress[lessonId] || {
                    completed: 0,
                    total: totalQuestions,
                    lastScore: 0,
                    attempts: 0
                };

                // Update the progress
                const updatedProgress = {
                    ...currentProgress,
                    completed: Math.max(currentProgress.completed, questionsCompleted),
                    total: totalQuestions,
                    lastScore: score,
                    lastCompletedDate: new Date().toISOString(),
                    attempts: currentProgress.attempts + 1
                };

                // Calculate new totals
                const allLessons = Object.values({
                    ...state.lessonProgress,
                    [lessonId]: updatedProgress
                });

                const totalStarted = allLessons.filter(l => l.attempts > 0).length;
                const totalCompleted = allLessons.filter(l => l.completed === l.total).length;
                const totalAnswered = allLessons.reduce((sum, l) => sum + l.completed, 0);

                // Calculate average score (only for lessons with attempts)
                const lessonsWithScores = allLessons.filter(l => l.lastScore > 0);
                const avgScore = lessonsWithScores.length > 0
                    ? Math.round(lessonsWithScores.reduce((sum, l) => sum + l.lastScore, 0) / lessonsWithScores.length)
                    : 0;

                return {
                    lessonProgress: {
                        ...state.lessonProgress,
                        [lessonId]: updatedProgress
                    },
                    totalQuestionsAnswered: totalAnswered,
                    totalLessonsStarted: totalStarted,
                    totalLessonsCompleted: totalCompleted,
                    averageScore: avgScore
                };
            });
        },

        // Reset progress for a specific lesson
        resetLessonProgress: (lessonId: string) => {
            update((state) => {
                const lessonProgress = { ...state.lessonProgress };

                if (lessonId in lessonProgress) {
                    lessonProgress[lessonId] = {
                        ...lessonProgress[lessonId],
                        completed: 0,
                        lastScore: 0,
                        attempts: 0
                    };
                }

                return {
                    ...state,
                    lessonProgress
                };
            });
        },

        // Reset all progress
        resetAllProgress: () => {
            set(initialState);
        }
    };
}

// Create the store
export const progressStore = createProgressStore();

// Derived store for badge status
export const badgeStatus = derived(progressStore, ($progress) => {
    const badges: Record<string, 'none' | 'bronze' | 'silver' | 'gold'> = {};

    Object.entries($progress.lessonProgress).forEach(([lessonId, progress]) => {
        if (progress.lastScore === 0) {
            badges[lessonId] = 'none';
        } else if (progress.lastScore >= 90) {
            badges[lessonId] = 'gold';
        } else if (progress.lastScore >= 75) {
            badges[lessonId] = 'silver';
        } else if (progress.lastScore >= 60) {
            badges[lessonId] = 'bronze';
        } else {
            badges[lessonId] = 'none';
        }
    });

    return badges;
});
