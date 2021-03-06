#include <WinSock2.h>
#include <Ws2tcpip.h>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <nfd.h>
#include <sstream>
#include <string>
#include <vector>

#pragma comment( lib, "ws2_32.lib" )
using namespace std;

const double GEAR           = 1 / 1.5;
const double MAX_DIST       = 200.0;
const double LEAD_DISTANCE  = 5;
const int    ONE_TURN_PULSE = 20000;

static NTSTATUS( __stdcall * NtDelayExecution )( BOOL Alertable, PLARGE_INTEGER DelayInterval ) = (NTSTATUS(
    __stdcall * )( BOOL, PLARGE_INTEGER )) GetProcAddress( GetModuleHandle( "ntdll.dll" ), "NtDelayExecution" );
static NTSTATUS( __stdcall * ZwSetTimerResolution )( IN ULONG RequestedResolution, IN BOOLEAN Set,
                                                     OUT PULONG ActualResolution ) =
    (NTSTATUS( __stdcall * )( ULONG, BOOLEAN, PULONG )) GetProcAddress( GetModuleHandle( "ntdll.dll" ),
                                                                        "ZwSetTimerResolution" );

static void SleepShort( float milliseconds )
{
  static bool once = true;
  if( once )
  {
    ULONG actualResolution;
    ZwSetTimerResolution( 1, true, &actualResolution );
    once = false;
  }

  LARGE_INTEGER interval;
  interval.QuadPart = -1 * (int) ( milliseconds * 10000.0f );
  NtDelayExecution( false, &interval );
}

int jog_pulse( double Gear, double AccessDistance, double LeadDistance, int OneTurnPulse )
{
  AccessDistance = clamp( AccessDistance, 0.0, MAX_DIST );
  return static_cast<int>( Gear * AccessDistance * OneTurnPulse / LeadDistance );
}

vector<vector<string>> read_csv( const string & filename )
{
  vector<vector<string>> data;
  vector<string>         row;

  ifstream file( filename );
  if( file.is_open() )
  {
    string line;
    while( getline( file, line ) )
    {
      stringstream lineStream( line );
      string       cell;
      while( getline( lineStream, cell, ',' ) ) { row.push_back( cell ); }
      data.push_back( row );
      row.clear();
    }
    file.close();
  }
  else
  {
    cout << "Error: Unable to open file " << filename << endl;
  }
  return data;
}

char * create_message( int line, int time, int x, int y, int z, int u, int v, int w )
{
  int x_counts = jog_pulse( GEAR, x, LEAD_DISTANCE, ONE_TURN_PULSE );
  int y_counts = jog_pulse( GEAR, y, LEAD_DISTANCE, ONE_TURN_PULSE );
  int z_counts = jog_pulse( GEAR, z, LEAD_DISTANCE, ONE_TURN_PULSE );
  int u_counts = jog_pulse( GEAR, u, LEAD_DISTANCE, ONE_TURN_PULSE );
  int v_counts = jog_pulse( GEAR, v, LEAD_DISTANCE, ONE_TURN_PULSE );
  int w_counts = jog_pulse( GEAR, w, LEAD_DISTANCE, ONE_TURN_PULSE );

  char * message = new char[50];
  message[0]     = (char) 0x55;    // ConfirmCode
  message[1]     = (char) 0xAA;
  message[2]     = (char) 0x00;    // PassWord
  message[3]     = (char) 0x00;
  message[4]     = (char) 0x14;    // FunctionCode
  message[5]     = (char) 0x01;
  message[6]     = (char) 0x00;    // ObjectChannel
  message[7]     = (char) 0x01;
  message[8]     = (char) 0xFF;    // WhoAcceptCode
  message[9]     = (char) 0xFF;
  message[10]    = (char) 0xFF;    // WhoReplyCode
  message[11]    = (char) 0xFF;
  message[12]    = (char) ( ( line >> 24 ) & 0xff );    // Line
  message[13]    = (char) ( ( line >> 16 ) & 0xff );
  message[14]    = (char) ( ( line >> 8 ) & 0xff );
  message[15]    = (char) ( ( line >> 0 ) & 0xff );
  message[16]    = (char) ( ( time >> 24 ) & 0xff );    // Time
  message[17]    = (char) ( ( time >> 16 ) & 0xff );
  message[18]    = (char) ( ( time >> 8 ) & 0xff );
  message[19]    = (char) ( ( time >> 0 ) & 0xff );
  message[20]    = (char) ( ( x_counts >> 24 ) & 0xff );    // X
  message[21]    = (char) ( ( x_counts >> 16 ) & 0xff );
  message[22]    = (char) ( ( x_counts >> 8 ) & 0xff );
  message[23]    = (char) ( ( x_counts >> 0 ) & 0xff );
  message[24]    = (char) ( ( y_counts >> 24 ) & 0xff );    // Y
  message[25]    = (char) ( ( y_counts >> 16 ) & 0xff );
  message[26]    = (char) ( ( y_counts >> 8 ) & 0xff );
  message[27]    = (char) ( ( y_counts >> 0 ) & 0xff );
  message[28]    = (char) ( ( z_counts >> 24 ) & 0xff );    // Z
  message[29]    = (char) ( ( z_counts >> 16 ) & 0xff );
  message[30]    = (char) ( ( z_counts >> 8 ) & 0xff );
  message[31]    = (char) ( ( z_counts >> 0 ) & 0xff );
  message[32]    = (char) ( ( u_counts >> 24 ) & 0xff );    // U
  message[33]    = (char) ( ( u_counts >> 16 ) & 0xff );
  message[34]    = (char) ( ( u_counts >> 8 ) & 0xff );
  message[35]    = (char) ( ( u_counts >> 0 ) & 0xff );
  message[36]    = (char) ( ( v_counts >> 24 ) & 0xff );    // V
  message[37]    = (char) ( ( v_counts >> 16 ) & 0xff );
  message[38]    = (char) ( ( v_counts >> 8 ) & 0xff );
  message[39]    = (char) ( ( v_counts >> 0 ) & 0xff );
  message[40]    = (char) ( ( w_counts >> 24 ) & 0xff );    // W
  message[41]    = (char) ( ( w_counts >> 16 ) & 0xff );
  message[42]    = (char) ( ( w_counts >> 8 ) & 0xff );
  message[43]    = (char) ( ( w_counts >> 0 ) & 0xff );
  message[44]    = (char) 0x00;    // Base Dout
  message[45]    = (char) 0x00;
  message[46]    = (char) 0x00;    // DAC 1/2
  message[47]    = (char) 0x00;
  message[48]    = (char) 0x00;
  message[49]    = (char) 0x00;

  return message;
}

void send_move_message( SOCKET sock, sockaddr_in dest, char * message )
{
  sendto( sock, message, 50, 0, (sockaddr *) &dest, sizeof( dest ) );
}

int main()
{
  const char * srcIP  = "";
  const char * destIP = "255.255.255.255";
  sockaddr_in  dest {};
  sockaddr_in  local {};
  WSAData      data {};
  WSAStartup( MAKEWORD( 2, 2 ), &data );

  local.sin_family = AF_INET;
  inet_pton( AF_INET, srcIP, &local.sin_addr.s_addr );
  local.sin_port = htons( 0 );

  dest.sin_family = AF_INET;
  inet_pton( AF_INET, destIP, &dest.sin_addr.s_addr );
  dest.sin_port = htons( 7408 );

  SOCKET s = socket( AF_INET, SOCK_DGRAM, IPPROTO_UDP );
  bind( s, (sockaddr *) &local, sizeof( local ) );
  char broadcast = 1;
  setsockopt( s, SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof( broadcast ) );

  char * min_slow = create_message( 1, 2000, 0, 0, 0, 0, 0, 0 );


  nfdchar_t * outPath = nullptr;
  nfdresult_t result  = NFD_OpenDialog( nullptr, nullptr, &outPath );

  if( result == NFD_OKAY )
  {
    vector<pair<char *, int>> messages;
    string                    filename = outPath;
    vector<vector<string>>    csv_data = read_csv( filename );

    if( csv_data.size() <= 1 ) cout << "\n\nNo Movement Data found. EXITING" << endl;

    cout << "\n\nCreating messages..." << endl;


    char * first_message = create_message( stoi( csv_data[1][0] ), 2000, stoi( csv_data[1][2] ), stoi( csv_data[1][3] ),
                                           stoi( csv_data[1][4] ), stoi( csv_data[1][5] ), stoi( csv_data[1][6] ),
                                           stoi( csv_data[1][7] ) );

    for( int i = 1; i < csv_data.size(); i++ )
    {
      int    line    = stoi( csv_data[i][0] );
      int    time    = stoi( csv_data[i][1] );
      int    x       = stoi( csv_data[i][2] );
      int    y       = stoi( csv_data[i][3] );
      int    z       = stoi( csv_data[i][4] );
      int    u       = stoi( csv_data[i][5] );
      int    v       = stoi( csv_data[i][6] );
      int    w       = stoi( csv_data[i][7] );
      char * message = create_message( line, time, x, y, z, u, v, w );
      messages.emplace_back( message, time );
      cout << "Line: " << line << " Time: " << time << " X: " << x << " Y: " << y << " Z: " << z << " U: " << u
           << " V: " << v << " W: " << w << endl;
    }

    cout << "\n\nSending messages..." << endl;

    if( !messages.empty() )
    {
      send_move_message( s, dest, first_message );
      SleepShort( 2000 );
    }

    for( auto & [message, time] : messages )
    {
      send_move_message( s, dest, message );
      SleepShort( time );
    }

    SleepShort( 1000 );
    cout << "\n\nSlowly moving down..." << endl;
    send_move_message( s, dest, min_slow );
  }
  else if( result == NFD_CANCEL )
  {
    cout << "User pressed cancel." << std::endl;
  }
  else
  {
    std::cout << "Error: " << NFD_GetError() << std::endl;
  }

  closesocket( s );
  WSACleanup();
  cout << "\n\nEnd of program..." << endl;
  return 0;
}
