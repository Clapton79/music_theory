# Music theory project

This project intends to help with music theory: display and play scales,
create simple midi format sound files a guitarist can practice with.

Later I will include features that help connecting scales over chord
progressions.

## Methods

| package       | method                    | comments                                                                                           |
|---------------|---------------------------|----------------------------------------------------------------------------------------------------|
|music_theory   | explore_scale             | explores a chord family by playing triads (alternating or not) in a descending or ascending fashion|
|               | find_note                 | finds the index of a note in the list of notes                                                     |                     
|               | get_chord                 | returns a list of what degrees and what alterations a chord has                                    |                                      
|               | get_chord_info            | breaks down a chord into parts, then looks up its notes                                            |                              
|               | get_chord_shape           | returns a list of what degrees and what alterations a chord has                                    |                                      
|               | get_list_note_ids			    | returns up the midi note id's of a list of notes                                                   |                       
|               | get_note_id        		    | searches for the midi note id                                                                      |    
|               | get_number 				        | removes the alphabetic elements of a text (this is to get the octave of the note)                  |
|               | get_scale 				        | returns a list for a scale                                                                         |
|               | get_scale_note 			      | returns the midi note id of the nth degree of a scale                                              |                            
|               | get_scale_triad 			    | get the 1st, 3rd, 5th of a scale in ascending or descending fashion                                |                                          
|               | get_text 					        | removes the numeric elements of a text (this is to get the note name)                              |                                            
