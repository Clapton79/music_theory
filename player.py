import music as M

M.renderDemos() # render some music wav files in ./

M.legacy.experiments.cristal2(.2, 300) # wav of sonic structure in ./

sound_waves=M.legacy.songs.madameZ(render=False) # return numpy array

sound_waves2=M.io.open("demosong2.wav") # numpy array

music=M.remix(sound_waves, soundwaves2)
music_=M.H(sound_waves[:44100*2], music[len(music)/2::2])

M.oi.write(music_)
