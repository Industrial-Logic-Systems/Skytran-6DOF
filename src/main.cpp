#include <WinSock2.h>
#include <Ws2tcpip.h>
#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <nfd.h>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

#pragma comment( lib, "ws2_32.lib" )
using namespace std;

// 400,000 = 170mm
// 0       = 3.5mm
// const int POS_MIN   = 0;
// const int POS_MAX   = 170;
// const int SCALE_MIN = 0;
// const int SCALE_MAX = 400000;

// const double GEAR                = 2.0;
// const double MAX_ACCESS_DISTANCE = 200.0;
// const double LEAD_DISTANCE       = 2.5;
// const int    ONE_TURN_PULSE      = 1000;

const double GEAR           = 1 / 1.5;
const double MAX_DIST       = 200.0;
const double LEAD_DISTANCE  = 5;
const int    ONE_TURN_PULSE = 20000;


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

  char * max = create_message( 1, 10, MAX_DIST, MAX_DIST, MAX_DIST, MAX_DIST, MAX_DIST, MAX_DIST );
  char * mid =
      create_message( 1, 10, MAX_DIST / 2, MAX_DIST / 2, MAX_DIST / 2, MAX_DIST / 2, MAX_DIST / 2, MAX_DIST / 2 );
  char * min      = create_message( 1, 10, 0, 0, 0, 0, 0, 0 );
  char * min_slow = create_message( 1, 2000, 0, 0, 0, 0, 0, 0 );

  bool run_custom = false;

  if( run_custom )
  {
    char * custom   = create_message( 1, 1000, 43, 43, 43, 43, 43, 43 );
    char * custom_1 = create_message( 1, 1000, 0, 121, 0, 121, 0, 121 );
    char * custom_2 = create_message( 1, 1000, 121, 0, 121, 0, 121, 0 );
    char * custom_3 = create_message( 1, 1000, 22, 65, 49, 49, 65, 22 );
    char * custom_4 = create_message( 1, 1000, 36, 61, 70, 20, 30, 55 );
    char * custom_5 = create_message( 1, 1000, 25, 25, 25, 25, 25, 25 );

    char * rest  = create_message( 1, 1000, 26, 26, 26, 26, 26, 26 );
    char * x_pos = create_message( 1, 1000, 38, 25, 43, 7, 2, 51 );
    char * x_neg = create_message( 1, 1000, 18, 31, 12, 48, 53, 4 );
    char * y_pos = create_message( 1, 1000, 51, 2, 7, 43, 25, 38 );
    char * y_neg = create_message( 1, 1000, 4, 53, 48, 12, 31, 18 );

    char * rest_100  = create_message( 1, 1000, 105, 105, 105, 105, 105, 105 );
    char * x_pos_max = create_message( 1, 1000, 155, 116, 171, 60, 43, 195 );
    char * x_neg_max = create_message( 1, 1000, 94, 135, 76, 186, 200, 49 );
    char * y_pos_max = create_message( 1, 1000, 195, 43, 60, 171, 116, 155 );
    char * y_neg_max = create_message( 1, 1000, 49, 200, 186, 76, 135, 94 );

    send_move_message( s, dest, rest );
    std::this_thread::sleep_for( std::chrono::milliseconds( 1000 ) );
    send_move_message( s, dest, x_pos_max );
    std::this_thread::sleep_for( std::chrono::milliseconds( 1000 ) );
    send_move_message( s, dest, rest );
    std::this_thread::sleep_for( std::chrono::milliseconds( 1000 ) );
    send_move_message( s, dest, x_neg_max );
    std::this_thread::sleep_for( std::chrono::milliseconds( 1000 ) );
    send_move_message( s, dest, rest );
    std::this_thread::sleep_for( std::chrono::milliseconds( 1000 ) );
    send_move_message( s, dest, y_pos_max );
    std::this_thread::sleep_for( std::chrono::milliseconds( 1000 ) );
    send_move_message( s, dest, rest );
    std::this_thread::sleep_for( std::chrono::milliseconds( 1000 ) );
    send_move_message( s, dest, y_neg_max );
    std::this_thread::sleep_for( std::chrono::milliseconds( 1000 ) );
    send_move_message( s, dest, min_slow );
  }
  else
  {
    nfdchar_t * outPath = nullptr;
    nfdresult_t result  = NFD_OpenDialog( nullptr, nullptr, &outPath );

    if( result == NFD_OKAY )
    {
      vector<pair<char *, int>> messages;
      string                    filename = outPath;
      vector<vector<string>>    csv_data = read_csv( filename );

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
        send_move_message( s, dest, messages[0].first );
        std::this_thread::sleep_for( std::chrono::milliseconds( 1000 ) );
      }

      for( auto & [message, time] : messages )
      {
        send_move_message( s, dest, message );
        std::this_thread::sleep_for( std::chrono::milliseconds( time ) );
      }

      std::this_thread::sleep_for( std::chrono::milliseconds( 1000 ) );
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
  }

  closesocket( s );
  WSACleanup();

  return 0;
}
