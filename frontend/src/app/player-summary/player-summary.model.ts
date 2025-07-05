// player-summary.model.ts

export interface Shot {
    isMake: boolean;
    locationX: number; // Measured in feet relative to the basket center
    locationY: number; // Measured in feet relative to the basket center
  }
  
  export interface Game {
    date: string; // ISO date string (e.g., "2022-12-19")
    isStarter: boolean;
    minutes: number;
    points: number;
    assists: number;
    offensiveRebounds: number;
    defensiveRebounds: number;
    steals: number;
    blocks: number;
    turnovers: number;
    defensiveFouls: number;
    offensiveFouls: number;
    freeThrowsMade: number;
    freeThrowsAttempted: number;
    twoPointersMade: number;
    twoPointersAttempted: number;
    threePointersMade: number;
    threePointersAttempted: number;
    shots: Shot[];
  }
  
  export interface PlayerSummary {
    name: string;
    games: Game[];
  }
  