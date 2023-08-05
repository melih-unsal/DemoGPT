# DemoGPT Development Roadmap

Our goal is to enable DemoGPT to accomplish anything that can be done through LangChain. In order to realize this goal, we have outlined the following development roadmap:

## Phase 1: New DemoGPT Pipeline Implementation

- Implement a new DemoGPT pipeline including plan generation, task creation, code snippet generation, and final code assembly.
- Define useful LangChain tasks and publish a release with the new pipeline without refinement.

## Phase 2: Model Selection and Integration

- Add a feature to allow users to select models that meet specific performance criteria.
- Integrate Llama 2 to DemoGPT for running everything locally.

## Phase 3: Task Implementation and Refinement

- Implement remaining LangChain tasks.
- Implement a self-refining strategy for model response refinement.

## Phase 4: API Integration and Expansion

- Integrate the Gorilla model for API calls.
- Add Rapid API for expanding available API calls.

## Phase 5: Database Implementation

- Implement a publicly available database to accelerate the generation process by retrieving similar examples during the refining process.
- Add all successfully generated steps to a DB to eliminate redundant refinement.

## Phase 6: Creation of React-Based Applications

- Extend DemoGPT's capabilities to create react-based applications, leveraging a self-refining strategy for continuous improvement of application performance.

This roadmap will guide our development efforts, and we look forward to sharing our progress with the community as we work towards making DemoGPT an indispensable tool for LangChain development.
