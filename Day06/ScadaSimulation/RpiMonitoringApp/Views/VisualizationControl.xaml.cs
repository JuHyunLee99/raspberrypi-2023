﻿using Google.Protobuf.WellKnownTypes;
using OxyPlot;
using OxyPlot.Series;
using MahApps.Metro.Controls;
using MySql.Data.MySqlClient;
using SmartHomeMonitoringApp.Logics;
using SmartHomeMonitoringApp.Models;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Ink;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using OxyPlot.Legends;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// VisualizationControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class VisualizationControl : UserControl
    {
        List<string> Divisions = null;
        string FirstSensingDate = string.Empty;

        int TotalDataCount = 0; // 검색된 데이터 개수

        public VisualizationControl()
        {
            InitializeComponent();
        }

        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            // 룸선택 콤보박스 초기화
            Divisions = new List<string> {"SELECT", "LIVING", "DINING", "BED", "BATH"};
            CboRoomName.ItemsSource = Divisions;
            CboRoomName.SelectedIndex = 0;  // SELECT가 기본 선택
            
            // 검색시작일 날짜 - DB에서 제일 오래된 날짜를 가져와서 할당
            using(MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
            {
                conn.Open();
                var dtQuery = @"SELECT F.Sensing_Date
                                  FROM (
                                   SELECT DATE_FORMAT(Sensing_DateTime, '%Y-%m-%d') AS Sensing_Date
                                      FROM smarthomesensor
                                ) AS F
                                 GROUP BY F.Sensing_Date
                                 ORDER BY F.Sensing_Date ASC Limit 1";  //  MYSQL 특징: Limit는 첫번째 데이터만 가져올수 있음
                MySqlCommand cmd = new MySqlCommand(dtQuery, conn);
                var result = cmd.ExecuteScalar();
                Debug.WriteLine(result.ToString());
                FirstSensingDate = DtpStart.Text = result.ToString();
                // 검색 종료일은 현재 일자 할당
                DtpEnd.Text = DateTime.Now.ToString("yyyy-MM-dd");
            }

        }

        // 컴색버튼 클릭 이벤트 핸들러
        private async void BtnSearch_Click(object sender, RoutedEventArgs e)
        {
            bool isValid = true;
            string errorMsg = string.Empty;
            DataSet ds = new DataSet(); // DB상에 있던 센싱데이터 담을 데이터셋

            // 검색, 저장, 수정, 삭제 전 반드시 검증(Validation)
            if (CboRoomName.SelectedValue.ToString() == "SELECT")
            {
                isValid = false;
                errorMsg += "방구분을 선택하세요.\n";
            }
            // 시스템 시작된 날짜보다 더 옛날 날짜로 검색하려면
            if (DateTime.Parse(DtpStart.Text) < DateTime.Parse(FirstSensingDate))
            {
                isValid = false;
                errorMsg += $"검색 시작일은 {FirstSensingDate}부터 가능합니다.\n";
            }

            // 오늘날짜 이후 날짜로 검색하려면
            if (DateTime.Parse(DtpEnd.Text) > DateTime.Now)
            {
                isValid = false;
                errorMsg += $"검색 종료일은 오늘까지 가능합니다.\n";
            }

            // 검색시작일이 검색종료일보다 이후면
            if (DateTime.Parse(DtpStart.Text) > DateTime.Parse(DtpEnd.Text))
            {
                isValid = false;
                errorMsg += $"검색 시작일이 검색 종료일보다 최신일 수 없습니다.";
            }

            if (isValid == false) 
            {
                // UserContrl같이 자식 클래스면서 MetroWindo를 직접 사용하지 않아, MahApps.Metro에 있는 Metro메세지창을 못쓸때 Commons이용해서 사용할수 있음.
                await Commons.ShowCustomMessageAsync("검색", errorMsg);
                return;
            }

            // 드디어 검색 시작
            TotalDataCount = 0;
            try
            {
            using(MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
            {
                    conn.Open();
                    var searchQuery = @"SELECT Id,
                                                Home_Id,
                                                Room_Name,
                                                Sensing_DateTime,
                                                Temp,
                                                Humid
                                            FROM smarthomesensor
                                            WHERE UPPER(Room_Name) = @Room_Name
	                                            AND date_format(Sensing_DateTime, '%Y-%m-%d')
                                            BETWEEN @StartDate AND @EndDate";

                    MySqlCommand cmd = new MySqlCommand(searchQuery, conn);
                    cmd.Parameters.AddWithValue("@Room_Name", CboRoomName.SelectedValue.ToString());
                    cmd.Parameters.AddWithValue("@StartDate", DtpStart.Text);
                    cmd.Parameters.AddWithValue("@EndDate", DtpEnd.Text);
                    MySqlDataAdapter adapter = new MySqlDataAdapter(cmd);

                    adapter.Fill(ds, "smarthomesensor");

                    // MessageBox.Show("TotalData", ds.Tables["smarthomesensor"].Rows.Count.ToString());
            }
            }
            catch (Exception ex)
            {

                await Commons.ShowCustomMessageAsync("DB검색", $"DB검색 오류 {ex.Message}");
            }

            // Create the plot model
            var tmp = new PlotModel { Title = $"{CboRoomName.SelectedValue} ROOM"};
            var legend = new Legend         // 범주
            {
                LegendBorder = OxyColors.DarkGray,  // 범주 박스 테두리 색상
                LegendBackground = OxyColor.FromArgb(150, 255, 255, 255),   // 범주 박스 백그라운드 색상
                LegendPosition = LegendPosition.TopRight,
                LegendPlacement = LegendPlacement.Outside,
            };
            tmp.Legends.Add(legend);    // 범례추가

            // Create two line series (markers are hidden by default)
            var tempSeries = new LineSeries 
            { 
                Title = "Temperature(℃)",
                MarkerType = MarkerType.Circle,
                Color= OxyColors.DarkOrange // 라인색상 온도 주황색
            };
            var humidSeries = new LineSeries 
            { 
                Title = "Humidity(%)",
                MarkerType = MarkerType.Square,
                Color = OxyColors.Aqua, // 라인색상 습도 아쿠아
            };

            // DB에서 가져온 데이터 차트에 뿌리도록 처리
            if (ds.Tables[0].Rows.Count > 0)
            {
                TotalDataCount = ds.Tables[0].Rows.Count;

                var count = 0;
                foreach (DataRow row in ds.Tables[0].Rows)
                {
                        // Convert.ToDouble(row["Temp"]);
                    tempSeries.Points.Add(new DataPoint(count++, Convert.ToDouble(row["Temp"])));
                    humidSeries.Points.Add(new DataPoint(count++, Convert.ToDouble(row["Humid"])));
                }

                // Add the series to the plot model
                tmp.Series.Add(tempSeries);
                tmp.Series.Add(humidSeries);
            }
            OpvSmartHome.Model = tmp;

            LblTotalCount.Content = $"검색데이터 {TotalDataCount}개";
        }
    }
}