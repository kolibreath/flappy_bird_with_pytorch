import pygame, sys, random
from bird import Bird
from game import Game
from genetic import Genetic

def handle_events(game, genetic, birds):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_start == False:
                    game.game_start = True

            # flyup event
            if event.type == pygame.USEREVENT + 2:
                index = event.index
                birds[index].bird_movement = 0
                birds[index].bird_movement -= game.move_up

            # restart game
            if event.type == pygame.MOUSEBUTTONDOWN and game.game_active == False:

                game.game_active = True
                game.pipe_list.clear()

                genetic.reset()

                game.score = 0

            if event.type == game.SPAWNPIPE:
                if game.game_start:
                    game.pipe_list.append(game.create_pipe())
                    remove_pipes(game.pipe_list)

            # birds flap animation
            if event.type == game.BIRDFLAP:
                # random choose some of the birds to display the animation
                indices = random.shuffle([i for i in range(genetic.pop_size)])
                for i in range(genetic.pop_size // 2):
                    bird = birds[i]
                    bird.bird_fly_index += 1
                    bird.bird_fly_index = bird.bird_fly_index % len(bird.bird_frames)
                    bird.bird_surface, bird.bird_rect = bird.bird_animation()

# show where the birds are 
def display_birds(game,birds):
    for bird_turple in birds: # bird_turple = (index, bird_instance)
        bird = bird_turple[1] # bird_instance
        rotated_bird = bird.rotate_bird(bird.bird_surface) # set bird animation
        bird.bird_movement += game.gravity                 # bird falling
        bird.bird_rect.centery += int(bird.bird_movement) 
        game.screen.blit(rotated_bird, bird.bird_rect)
# spwan pipes
def spwan_pipes(game):
    game.pipe_list = game.move_pipes(game.pipe_list)
    game.draw_pipes(game.pipe_list)
    
# remove pipes from list that get out of the screen
def remove_pipes(pipe_list):
    for pipe_rect in pipe_list:
        if pipe_rect[0].bottomright[0] < 0 or pipe_rect[1].bottomright[0] < 0:
            pipe_list.remove(pipe_rect)
 


# where the game begins
if __name__ == "__main__":
    
    game = Game()  # initialize Game instance
    game.start()  # set timer
    
    genetic = Genetic(game, pop_size= 1 , generation= 30)
    birds = genetic.init_pop()
    
    # Game Logic
    while True:
        game.screen.blit(game.bg_surface, (0, 0)) # draw background image 
        game.draw_floor() # draw floor
        
        # game is not started, right click the screen to start the game
        if game.game_start == False:
            game.screen.blit(game.game_start_surface, game.game_start_rect)
            
        # event loop
        handle_events(game, genetic, birds)

        # one generation is not over
        if game.game_active and game.game_start:
            genetic.run_GA()
            for bird in birds:
                game.check_collision(game.pipe_list, bird)
            
            alive_birds = genetic.check_alive()
            if len(alive_birds) ==  0:
                game_active = False
            else:
                game_active = True
                
            #todo 修改了顺序 我觉得应该也是没有问题的
            display_birds(game, alive_birds)
            spwan_pipes(game)

            # 计算分数
            game.score += 0.01
            game.score_display('main_game', genetic)

        # One generation over
        if game.game_active == False and game.game_start:
            if game.score > game.high_score:
                high_score = game.score
            game.screen.blit(game.game_over_surface, game.game_over_rect)
            game.score_display('game_over', genetic)
            
            game.generation += 1
            
            # todo 
            if game.generation == 30:
                game.score_display('game_over', genetic)
                sys.exit()
        pygame.display.update()
        game.clock.tick(120)
