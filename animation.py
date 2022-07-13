def animate(self, animation_type):
    """TODO: interrupt animations ?"""
    match animation_type:
        case 'walk':
            # animate
            return
        case 'run':
            #animate
            return
        case 'jump':
            #animate
            return


"""
button_pos = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
s = pygame.Surface((140, 40))
s.set_alpha(10)
# if the mouse is in the button but this is the first frame she is in.
if SCREEN_WIDTH/2 <= self.mouse_pos[0] <= SCREEN_WIDTH/2+140 and SCREEN_HEIGHT/2 <= self.mouse_pos[1] <= SCREEN_HEIGHT/2+40:
    self.is_in_button = True
else:
    self.is_in_button = False


if self.is_in_button and self.there_is_already_a_button:
    return
elif self.is_in_button and not self.there_is_already_a_button:
    s.fill(LIGHT_COLOR)
    self.there_is_already_a_button = True
self.background_img.blit(s, button_pos)
"""