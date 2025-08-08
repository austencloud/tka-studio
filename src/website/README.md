# The Kinetic Constructor

![The Kinetic Constructor](static/pwa/icon-192x192.png)

A modern web application for creating, visualizing, and sharing kinetic sequences and pictographs.

## Overview

The Kinetic Constructor is a powerful web-based tool designed for creating and visualizing kinetic sequences. It provides an intuitive interface for constructing pictographs, generating sequences, and exploring kinetic patterns. The application is built with modern web technologies and follows a component-based architecture for maximum flexibility and maintainability.

## Features

### Core Features

- **Pictograph Visualization**: Create and visualize pictographs with customizable props, arrows, and grid layouts.
- **Sequence Generation**: Generate sequences using circular or freeform patterns with adjustable parameters.
- **Interactive Grid System**: Work with diamond or box grid layouts for precise positioning.
- **State Management**: Robust state management using XState and Svelte stores.
- **Responsive Design**: Fully responsive interface that works on desktop, tablet, and mobile devices.
- **Progressive Web App**: Install as a standalone application on supported devices.

### Key Components

- **Pictograph Component**: Visualizes kinetic movements with props, arrows, and grid.
- **Sequence Workbench**: Create and edit sequences with an intuitive interface.
- **Generate Tab**: Generate sequences with customizable parameters.
- **Grid System**: Provides the foundation for positioning elements.
- **TKA Glyphs**: Renders specialized kinetic notation.

## Technology Stack

- **Frontend Framework**: [Svelte](https://svelte.dev/) / [SvelteKit](https://kit.svelte.dev/)
- **State Management**:
  - [XState](https://xstate.js.org/) for complex state machines
  - Svelte stores for reactive state
- **Styling**: [TailwindCSS](https://tailwindcss.com/) for utility-first styling
- **Deployment**: [Netlify](https://www.netlify.com/) for hosting and serverless functions
- **Testing**: [Vitest](https://vitest.dev/) for unit and integration testing
- **Icons**: [FontAwesome](https://fontawesome.com/) and [Lucide](https://lucide.dev/)
- **Animation**: [Svelte Motion](https://svelte-motion.gradientdescent.de/) for fluid animations

## Architecture

The application follows a modern architecture with these key principles:

### State Management

The application uses a tiered approach to state management:

1. **Application Core (XState)**: For complex, stateful workflows like application lifecycle, authentication flows, and multi-step processes.
2. **Feature State (Svelte Stores)**: For feature-specific state like domain data, feature settings, and UI state.
3. **Component State (Svelte reactivity)**: For component-level state like form inputs, local UI state, and temporary visual state.

All state containers are registered with a central registry for debugging, persistence, and testing.

### Dependency Injection

The application implements a modern dependency injection system to improve modularity, testability, and maintainability by:

- Centralizing service creation and management
- Replacing manual dependency handling with automated injection
- Eliminating problematic singleton patterns
- Enabling easier mocking for tests

### Component Structure

Components are organized by feature and follow a consistent pattern:

- **Main Components**: High-level components that compose multiple sub-components
- **UI Components**: Reusable UI elements with specific styling and behavior
- **Feature Components**: Components specific to a feature or domain
- **Service Components**: Components that provide services to other components

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (v16 or later)
- npm (included with Node.js)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/the-kinetic-constructor-web.git
   cd the-kinetic-constructor-web
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm run dev
   ```

4. Open your browser and navigate to [http://localhost:5173](http://localhost:5173)

### Building for Production

```bash
npm run build
```

The built application will be in the `build` directory.

### Running Tests

```bash
# Run all tests
npm test

# Run tests with watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

## Project Structure

```
the-kinetic-constructor-web/
├── src/
│   ├── app.html           # Main HTML template
│   ├── lib/               # Library code
│   │   ├── components/    # Svelte components
│   │   │   ├── GenerateTab/       # Sequence generation components
│   │   │   ├── MainWidget/        # Main application widget
│   │   │   ├── objects/           # Core object components (Grid, Prop, Arrow, etc.)
│   │   │   ├── OptionPicker/      # Option selection components
│   │   │   ├── Pictograph/        # Pictograph visualization components
│   │   │   └── SequenceWorkbench/ # Sequence editing components
│   │   ├── context/       # Svelte context providers
│   │   ├── services/      # Application services
│   │   ├── state/         # State management
│   │   │   ├── core/      # Core state utilities
│   │   │   ├── machines/  # XState machines
│   │   │   └── stores/    # Svelte stores
│   │   ├── types/         # TypeScript type definitions
│   │   └── utils/         # Utility functions
│   ├── routes/            # SvelteKit routes
│   └── tests/             # Test files
├── static/                # Static assets
├── docs/                  # Documentation
├── tailwind.config.ts     # TailwindCSS configuration
├── svelte.config.js       # Svelte configuration
├── vite.config.ts         # Vite configuration
└── package.json           # Project dependencies and scripts
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Svelte](https://svelte.dev/) and [SvelteKit](https://kit.svelte.dev/) for the amazing framework
- [XState](https://xstate.js.org/) for the powerful state machine implementation
- [TailwindCSS](https://tailwindcss.com/) for the utility-first CSS framework
- [Netlify](https://www.netlify.com/) for hosting and serverless functions
- All the open-source libraries that made this project possible
