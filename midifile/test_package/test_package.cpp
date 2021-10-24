#include <MidiFile.h>
#include <random>

int main (int argc, char * argv[]) 
{
	::smf::MidiFile midifile;
	int track   = 0;
	int channel = 0;
	int instr   = 0;
	midifile.addTimbre(track, 0, channel, instr);

	std::random_device rd;
	std::mt19937 mt(rd());
	std::uniform_int_distribution<int> starttime(0, 100);
    std::uniform_int_distribution<int> duration(1, 8);
    std::uniform_int_distribution<int> pitch(36, 84);
    std::uniform_int_distribution<int> velocity(40, 100);

	int tpq     = midifile.getTPQ();
	int count   = 10;
	for(int i=0 ; i<count ; ++i) 
	{
		int starttick = static_cast<int>(starttime(mt) / 4.0 * tpq);
		int key       = pitch(mt);
		int endtick   = starttick + int(duration(mt) / 4.0 * tpq);
		midifile.addNoteOn (track, starttick, channel, key, velocity(mt));
		midifile.addNoteOff(track, endtick,   channel, key);
	}

    return EXIT_SUCCESS;
}
