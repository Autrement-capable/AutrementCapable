# BETA TEST PLAN – AUTREMENT CAPABLE

## 1. Core Functionalities for Beta Version

This Beta Test Plan focuses on the MVP features available to young neurodivergent users (primarily with Autism Spectrum Disorder) after one year of development. The platform is a gamified, accessible self-discovery journey built to help them build confidence, understand themselves, and prepare for the future.

| **Feature Name**                | **Description**                                                                                                                      | **Priority** | **Changes Since Tech3**                         |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------ | ----------------------------------------------- |
| Personalized Profile Generation | A dynamic profile is generated from game inputs and evolves in real-time, helping the user discover their strengths and preferences. | Medium       | New addition based on gameplay data integration |
| Passwordless Onboarding         | Secure and inclusive onboarding using Passkey authentication (no passwords).                                                         | High         | Integrated with accessibility-first design      |
| AI Avatar Generation            | Custom AI-based avatar creation to help users identify with their digital persona.                                                   | Medium       | Added emotional expression options              |
| Guided Dashboard & Badge System | Minimalist dashboard showing progress through visual badges and a central evolving badge.                                            | High         | Co-designed with autism specialists             |
| Accessibility Widget            | A floating tool allowing on-the-fly accessibility adaptations (text size, audio, contrast, etc.).                                    | High         | Almost Fully integrated into all pages          |
| 6 Mini-Games for Self-Discovery | Interactive modules that help build the user profile across logic, typing, preferences, and soft skills.                             | High         | Co-designed with autistic youth and experts     |

## 2. Beta Testing Scenarios

### 2.1 User Role

Only one role is involved in the MVP testing phase.

| **Role Name** | **Description**                                                                             |
| ------------- | ------------------------------------------------------------------------------------------- |
| Young User    | A neurodivergent teenager discovering their strengths and preferences through the platform. |

### 2.2 Test Scenarios

#### Scenario 1: Onboarding Flow

- **Role Involved:** User
- **Objective:** Creating Avatar & choose visual personalization.
- **Preconditions:** Have a computer.
- **Test Steps:**
  1. Start onboarding process.
  2. Choose prefered theme background.
  3. Personal information (Name, age).
  4. Creating avatar based on questions.
- **Expected Outcome:** Avatar and background reflect user's identity and preferences.

#### Scenario 2: Register using Passkey

- **Role Involved:** User
- **Objective:** Create an account easily.
- **Preconditions:** Creating Avatar & choose visual personalization.
- **Test Steps:**
  1. Finish avatar creation.
  2. Account creation without password.
- **Expected Outcome:** Created an account in seconds without the need of user name and password.

#### Scenario 3: Dashboard & Badge Progression Explanation

- **Role Involved:** User
- **Objective:** Understanding of the dashboard and badges progression.
- **Preconditions:** Finished the onboarding.
- **Test Steps:**
  1. Following steps from the guide to explore dashboard features.
  2. Following steps from the guide to explore badges progression.
  3. Start your first game.
- **Expected Outcome:** The user must have understand all features and dashboard.

#### Scenario 4: Game Modules (Self-Discovery Path)

- **Role Involved:** User
  Each game contributes to enriching the user's profile. They are:

| **Game**               | **Objective**                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------------- |
| Passion Explorer       | Watch job videos and rate them (like/dislike/unsure) to identify interests.                 |
| Ideal Work Environment | Customize a 3D room (light, noise, people, etc.) to define preferred workspace.             |
| Typing Ability         | Type increasingly difficult words to assess motor/typing skills.                            |
| Logical Thinking       | Solve sequences of shapes to test user logic.                                               |
| Skill Self-Assessment  | Find if the user has a skills, want to develop it or doesn't have it.                       |
| Emotional Intelligence | Choose reactions to life/workplace situations to assess emotional response and soft skills. |

- **Preconditions:** Finish scenario 3.
- **Test Steps:**

  1.  Do games.
  2.  See your new badges.
  3.  See your profile progression.

- **Expected Outcome:** Game completes; data is stored and shown in profile/badges.

## 3. Success Criteria

| **Metric**              | **Description**                                                   | **Target Threshold**                     |
| ----------------------- | ----------------------------------------------------------------- | ---------------------------------------- |
| Onboarding Completion   | Successful Passkey registration and personalization.              | 95%                                      |
| Game Completion Rate    | Users who finish 4 out of 6 mini-games.                           | ≥ 80%                                    |
| Badge Unlock Rate       | Users who unlock at least 3 individual badges.                    | ≥ 85%                                    |
| Interface Understanding | Users report dashboard and progression are easy to understand.    | ≥ 90% satisfaction (from post-test form) |
| Comfort & Engagement    | Users feel safe, curious, and comfortable engaging with the tool. | ≥ 85% positive feedback                  |

## 4. Known Issues & Limitations

| **Issue**                     | **Description**                                                     | **Impact** | **Planned Fix?** |
| ----------------------------- | ------------------------------------------------------------------- | ---------- | ---------------- |
| 3D Room Lag                   | Environment builder may lag on old phones/tablets.                  | Low        | No               |
| Passkey Browser Compatibility | Limited support on Android and not supported on most Linux devices. | Low        | No               |
| Overlapping UI Elements       | Accessibility widget may overlap with some animated elements.       | High       | Yes              |
| Dashboard Background Lag      | Slight performance issues with background effects on older devices. | Medium     | Yes              |

## 5. Conclusion

This MVP Beta Test Plan focuses on delivering an accessible, personalized, and gamified self-discovery experience for autistic youth. By validating core flows like onboarding, interactive games, badge progression, and interface clarity, this test phase will shape a tool that empowers neurodivergent users to understand themselves, gain confidence, and take early steps toward a fulfilling professional future.
