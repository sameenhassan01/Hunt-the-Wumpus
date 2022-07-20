#include <time.h>
#include <iostream>
#include <sstream>
#include<string>
using namespace std;

typedef unsigned char byte;

enum gResult { finish, newplayer };
enum object : byte { nothng, wump = 1, pit = 4, player = 8 };

const unsigned S_player = 0, S_wump = 1, S_pit1 = 4, S_pit2 = 5,
max_Rooms = 30, saved = 6, max_Exits = 3, Path_Length = 5, maximum_Arrows = 5;



class Rooms_available
{
public:
	int getExit(int i) { return exits[i]; }
	byte conntains() { return obj; }
	void Clear(object o) { obj ^= o; }
	void ClearRoom() { obj = nothng; }
	void setExit(int i, int e) { exits[i] = e; }
	void Populate(object o) { obj |= o; }


private:
	int exits[max_Exits];
	byte obj;
};
class movement
{
public:
	int playagain(std::string s, int a, int b)
	{
		int c;
		do
		{
			message(s);
			std::string r; std::cin >> r;
			std::cin.clear(); std::cin.ignore();
			c = toupper(r[0]);
		} while (c != a && c != b);

		return c;
	}

	int Number(std::string s)
	{
		int n = 0; std::string c;
		while (true)
		{
			message(s);
			std::getline(std::cin, c);
			std::stringstream strm(c);
			if (strm >> n) break;
		}
		return n;
	}

	void message(std::string s) { std::cout << s; }
	void message(int i) { std::cout << i; }
	void Wait() { std::cin.get(); }
};



class Caves
{
public:
	Caves()
	{
		int conn[] = { 1, 4, 7, 0, 2, 9, 1, 3, 11, 2, 4, 13, 0, 3, 5, 4, 6, 14, 5, 7, 16, 0, 6, 8, 7, 9, 17, 1, 8, 10, 9, 11, 18,
		2, 10, 12, 11, 13, 19, 3, 12, 14, 5, 13, 15, 14, 16, 19, 6, 15, 17, 8, 16, 18, 10, 17, 19, 12, 15, 18 };

		for (int x = 0, r = 0; x < max_Rooms; x++, r = x * max_Exits)
		{
			for (unsigned c = r, d = 0; c < r + max_Exits; c++, d++)
				Rooms_availables[x].setExit(d, conn[c]);
		}
		Clear();
	}

	void Clear()
	{
		for (int x = 0; x < max_Rooms; x++)
			Rooms_availables[x].ClearRoom();
	}

	Rooms_available* getRoom(int i) { return &Rooms_availables[i]; }

private:
	Rooms_available Rooms_availables[max_Rooms];
};

class Wumps
{
private:
	movement M;
	Caves C;
	unsigned playerPos, Wumpus_inPos, arrowsCnt, exits[max_Exits], saved[saved];
	bool gameOver, playerWins;

	void Look_out()
	{
		Rooms_available* r = C.getRoom(playerPos);
		M.message("You are in Rooms ::"); M.message(playerPos + 1);
		M.message("Rooms available nearby  : ");
		for (int x = 0; x < max_Exits; x++)
		{
			M.message((1 + r->getExit(x)));
			M.message(" ");
		}

		nearby_wumpus(r);
	}

	gResult showResult(bool pw)
	{
		if (pw) M.message("\n You got the Wumpus!\n\n");
		else M.message(" You lose!\n\n");

		if (M.playagain("Play again (Y/N)? ", 'Y', 'N') == 'Y')
		{
			;
			return newplayer;
		}

		return finish;
	}

	void nearby_wumpus(Rooms_available* r)
	{
		byte message = 0, o;
		for (int x = 0; x < max_Exits; x++)
		{
			o = C.getRoom(r->getExit(x))->conntains();
			message += ((wump & o)  + (pit & o));
		}

		if (message & wump) M.message("\nYou smell something terrible nearby.");
		if (message & pit) M.message("\nYou feel a cold wind blowing from a nearby Caves_availablern.");
		
	}

	bool checkExits(int e)
	{
		for (int x = 0; x < max_Exits; x++)
			if (e == exits[x]) return true;
		return false;
	}

	void getInput()
	{
		if (M.playagain("\n\n Want to move press  M :",' ' ,  'M') == 'M')
		{
			int e = M.Number("Where to? ") - 1;
			if (checkExits(e)) Set_PLAYER(e);
			else M.message("\n You cannot go there!\n\n");
		}
		
	}

	void Set_PLAYER(int pos)
	{
		if (playerPos < max_Rooms)
			C.getRoom(playerPos)->Clear(player);

		if (Hazards_around(pos)) return;

		playerPos = pos;
		Rooms_available* r = C.getRoom(playerPos);
		r->Populate(player);

		for (int x = 0; x < max_Exits; x++)
			exits[x] = r->getExit(x);
	}

	bool Hazards_around(int pos)
	{
		Rooms_available* r = C.getRoom(pos);
		byte o = r->conntains();

		if (wump & o)
		{
			M.message("\n OOPS! a Wumpus!\n\n");
			if (Wumpus_inMove(pos))
			{
				M.message("\n Wumpus got you!\n");
				gameOver = true; playerWins = false;
				return true;
			}
		}

		if (pit & o)
		{
			M.message("\n you Fell in pit sorry \n");
			gameOver = true; playerWins = false;
			return true;
		}

		

		return false;
	}

	bool Wumpus_inMove(int pos)
	{
		if (rand() % 100 < 75)
		{
			Rooms_available* r = C.getRoom(Wumpus_inPos);
			r->Clear(wump);
			Wumpus_inPos = r->getExit(rand() % max_Exits);
			C.getRoom(Wumpus_inPos)->Populate(wump);
		}
		return (pos == Wumpus_inPos);
	}

	void Init_GAME(gResult gr)
	{
		M.message("\n\n\n\n welcome the HUNT THE Wumps Game \n\n");
		C.Clear(); gameOver = false; arrowsCnt = maximum_Arrows;

		if (gr == newplayer)
		{
			saved[S_player] = rand() % max_Rooms;
			Set_PLAYER(saved[S_player]);
			saved[S_pit1] = Fill_ROOM(pit); saved[S_pit2] = Fill_ROOM(pit);
			Wumpus_inPos = saved[S_wump] = Fill_ROOM(wump);
		}
		else
		{
			Set_PLAYER(saved[S_player]); Wumpus_inPos = saved[S_wump];
			C.getRoom(Wumpus_inPos)->Populate(wump);
			C.getRoom(saved[S_pit1])->Populate(pit);
			C.getRoom(saved[S_pit2])->Populate(pit);
		}
	}

	int Fill_ROOM(object c)
	{
		int i; Rooms_available* r;
		do
		{
			i = rand() % max_Rooms;
			r = C.getRoom(i);
		} while (r->conntains());

		r->Populate(c);
		return i;
	}

public:
	void play()
	{
		playerPos = max_Rooms;
		gResult gr = newplayer;

		

		while (gr != finish)
		{
			Init_GAME(gr);
			while (!gameOver) { Look_out(); getInput(); }
			gr = showResult(playerWins);
		}
	}
};

int main(int argc, char* argv[])
{
	
	Wumps W; W.play();
	return 0;
}
