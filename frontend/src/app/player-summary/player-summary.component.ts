import {
  ChangeDetectorRef,
  Component,
  OnDestroy,
  OnInit,
  ViewEncapsulation
} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { untilDestroyed, UntilDestroy } from '@ngneat/until-destroy';
import { PlayersService } from '../_services/players.service';
import { PlayerSummary } from './player-summary.model'; // Import the interface

@UntilDestroy()
@Component({
  selector: 'player-summary-component',
  templateUrl: './player-summary.component.html',
  styleUrls: ['./player-summary.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class PlayerSummaryComponent implements OnInit, OnDestroy {

  playerSummary: PlayerSummary; // Declare the property
  playerId: number = 1; // Default player ID for testing
  gameId: number; // Holds game ID input from user

  constructor(
    protected activatedRoute: ActivatedRoute,
    protected cdr: ChangeDetectorRef,
    protected playersService: PlayersService,
  ) { }

   ngOnInit(): void {
    this.fetchPlayerSummary(); // Load default player data on initialization
  }

  fetchPlayerSummary(): void {
    console.log(`Fetching data for player ID: ${this.playerId}`);

    this.playersService.getPlayerSummary(this.playerId)
      .subscribe(
        (data) => {
          this.playerSummary = data.apiResponse; // Assign the fetched data
          console.log('Player Summary:', this.playerSummary);
          this.cdr.markForCheck(); // Trigger change detection
        },
        (error) => {
          console.error('Error fetching player summary:', error);
        }
      );
  }
  convertFeetToPixels(feet: number): number {
    const pixelsPerFoot = 10; // Adjust this based on the court image's scale
    return feet * pixelsPerFoot;
  }
  ngOnDestroy() { }
}
