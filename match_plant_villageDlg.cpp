
// match_plant_villageDlg.cpp : 实现文件
//

#include "stdafx.h"
#include "match_plant_village.h"
#include "match_plant_villageDlg.h"
#include "afxdialogex.h"
#include <iostream>
using namespace std;
#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// 用于应用程序“关于”菜单项的 CAboutDlg 对话框

class CAboutDlg : public CDialogEx
{
public:
	CAboutDlg();

// 对话框数据
	enum { IDD = IDD_ABOUTBOX };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 支持

// 实现
protected:
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialogEx(CAboutDlg::IDD)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialogEx)
END_MESSAGE_MAP()


// Cmatch_plant_villageDlg 对话框



Cmatch_plant_villageDlg::Cmatch_plant_villageDlg(CWnd* pParent /*=NULL*/)
	: CDialogEx(Cmatch_plant_villageDlg::IDD, pParent)
	, m_FilePath(_T(""))
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void Cmatch_plant_villageDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Text(pDX, IDC_EDIT_PATH, m_FilePath);
}

BEGIN_MESSAGE_MAP(Cmatch_plant_villageDlg, CDialogEx)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_BN_CLICKED(IDC_BTN_SELECT_IMAGE_PATH, &Cmatch_plant_villageDlg::OnBnClickedBtnSelectImagePath)
	ON_BN_CLICKED(IDC_BTN_CUT_IMAGE, &Cmatch_plant_villageDlg::OnBnClickedBtnCutImage)
	ON_BN_CLICKED(IDC_BUTTON1, &Cmatch_plant_villageDlg::OnBnClickedButton1)
	ON_BN_CLICKED(IDC_BUTTON2, &Cmatch_plant_villageDlg::OnBnClickedButton2)
END_MESSAGE_MAP()


// Cmatch_plant_villageDlg 消息处理程序

BOOL Cmatch_plant_villageDlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// 将“关于...”菜单项添加到系统菜单中。

	// IDM_ABOUTBOX 必须在系统命令范围内。
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		BOOL bNameValid;
		CString strAboutMenu;
		bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
		ASSERT(bNameValid);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// 设置此对话框的图标。当应用程序主窗口不是对话框时，框架将自动
	//  执行此操作
	SetIcon(m_hIcon, TRUE);			// 设置大图标
	SetIcon(m_hIcon, FALSE);		// 设置小图标

	// TODO: 在此添加额外的初始化代码
	AllocConsole();                                          // 开辟控制台
	SetConsoleTitle(_T("拆分xml"));     
	freopen("CONOUT$","w",stdout);
	freopen( "CONIN$", "r+t", stdin );
	return TRUE;  // 除非将焦点设置到控件，否则返回 TRUE
}

void Cmatch_plant_villageDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialogEx::OnSysCommand(nID, lParam);
	}
}

// 如果向对话框添加最小化按钮，则需要下面的代码
//  来绘制该图标。对于使用文档/视图模型的 MFC 应用程序，
//  这将由框架自动完成。

void Cmatch_plant_villageDlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // 用于绘制的设备上下文

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// 使图标在工作区矩形中居中
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// 绘制图标
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialogEx::OnPaint();
	}
}

//当用户拖动最小化窗口时系统调用此函数取得光标
//显示。
HCURSOR Cmatch_plant_villageDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}


//选择路径
void Cmatch_plant_villageDlg::OnBnClickedBtnSelectImagePath()
{
	
		// TODO: 在此添加控件通知处理程序代码

		CFileDialog dlg(TRUE);///TRUE为OPEN对话框，FALSE为SAVE AS对话框  
		CString csDirParth;  
		if(dlg.DoModal()==IDOK)  
			m_FilePath = dlg.GetPathName();  
		else  
			m_FilePath.Empty();  

		int iEndPos = 0;  
		iEndPos = m_FilePath.ReverseFind('\\');  
		csDirParth = m_FilePath.Left(iEndPos);
		m_FilePath=csDirParth;
		UpdateData(FALSE);
}


 void Cmatch_plant_villageDlg::OnBnClickedBtnCutImage()
	{
		// TODO: 在此添加控件通知处理程序代码

		CString  csDirPath=m_FilePath+"\\*.jpg"; 
		HANDLE file;  
		WIN32_FIND_DATA fileData;  
		char line[1024];  
		char fn[1000];  
		//mbstowcs(fn,csDirPath.GetBuffer(),999);  
		file = FindFirstFile(csDirPath.GetBuffer(), &fileData);  
		bool bState = false;  
		bState = FindNextFile(file, &fileData);  
		while(bState){  
			//对图像进行分块处理
			imageProcess(m_FilePath+"\\"+fileData.cFileName);

			bState = FindNextFile(file, &fileData);  
			UpdateWindow();
		}  
	}
void Cmatch_plant_villageDlg::imageProcess(CString imagePath)
{
	IplImage *pOrginImage=cvLoadImage(imagePath);
	CString save_image_path="G:\\test1\\";
	if(pOrginImage!=NULL)
	{
		int i,j;
		int width = pOrginImage->width;
		int height = pOrginImage->height;
		IplImage *pDestImage=cvCreateImage(cvGetSize(pOrginImage),pOrginImage->depth,pOrginImage->nChannels);
		IplImage* imgYUV = cvCreateImage(cvGetSize(pOrginImage),pOrginImage->depth,pOrginImage->nChannels);
		IplImage* y_plane = cvCreateImage( cvGetSize(imgYUV), IPL_DEPTH_8U, 1 );
		IplImage* u_plane = cvCreateImage( cvGetSize(imgYUV), IPL_DEPTH_8U, 1 );
		IplImage* v_plane = cvCreateImage( cvGetSize(imgYUV), IPL_DEPTH_8U, 1 );
		IplImage* gray_image = cvCreateImage( cvGetSize(imgYUV), IPL_DEPTH_8U, 1 );
		cvCopyImage(pOrginImage,pDestImage);
		//cvZero(gray_image);
		//转换颜色空间-将RGB空间转为YUV
		cvCvtColor(pOrginImage,imgYUV,CV_BGR2YUV);
		//转为灰度图像
		cvCvtColor(pOrginImage,gray_image,CV_RGB2GRAY);
		//获取各个空间分量
		cvCvtPixToPlane(imgYUV, y_plane, u_plane, v_plane,0);
		cvThreshold(v_plane,gray_image,0,255,CV_THRESH_OTSU | CV_THRESH_BINARY_INV);
		cvSmooth(gray_image,gray_image,CV_MEDIAN,3);
		

		int minx,miny,maxx,maxy;
		minx=width;
		miny=height;
		maxx=0;
		maxy=0;

		for(int i=0;i<height;i++)
		{
			for(int j=0;j<width;j++)
			{
				double pixel=cvGetReal2D(gray_image,i,j);
				if(pixel==255)
				{
					if(j<minx)
					{
						minx=j;
					}
					if(i<miny)
					{
						miny=i;
					}
					if(j>maxx)
					{
						maxx=j;
					}
					if(i>maxy)
					{
						maxy=i;
					}
				}
			}
		}
		//cvThreshold(gray_image,gray_image,0,255,CV_THRESH_OTSU );
		
		/*float valH,valS,valV;
		for(j=0;j<height;j++) 
		{	
			uchar* ptrH = (uchar*)(y_plane->imageData+y_plane->widthStep*j);
			uchar* ptrS = (uchar*)(u_plane->imageData+u_plane->widthStep*j);
			uchar* ptrV = (uchar*)(v_plane->imageData+v_plane->widthStep*j);
			uchar* ptrD = (uchar*)(pOrginImage->imageData+pOrginImage->widthStep*j);
			for(i=0;i<width;i++)
			{	
				valH = (float)ptrH[i];
				valS = (float)ptrS[i];
				valV = (float)ptrV[i];
				if( valV>110)
				{
					cvSet2D(pOrginImage,j,i,CV_RGB(0,0,0));
				}
			}
		}*/
	    cout<<imagePath<<endl;
		int imageNamePos=imagePath.ReverseFind('.');
		int imageNamePos2=imagePath.ReverseFind('\\');
		int imageNameLen=imagePath.GetLength();
		CvRect rect;
		rect.x=minx;
		rect.y=miny;
		rect.height=maxy-miny;
		rect.width=maxx-minx;
		cvSetImageROI(pDestImage,rect);
		CString imageName=imagePath.Right(imageNameLen-imageNamePos2-1);
		cout<<imageName<<endl;
		//CString imageName=imagePath.Mid(imageNamePos2+1,imageNamePos-imageNamePos2-1);
		save_image_path=save_image_path+imageName;
		cvSaveImage(save_image_path,pDestImage);
		cvResetImageROI(pDestImage);
		save_image_path="G:\\test1\\";
		imageName="";
		//释放内存
		cvReleaseImage(&pOrginImage);
		cvReleaseImage(&pDestImage);
		cvReleaseImage(&imgYUV);
		cvReleaseImage(&y_plane);
		cvReleaseImage(&u_plane);
		cvReleaseImage(&v_plane);
		cvReleaseImage(&gray_image);
	}
}
//打开文件夹
void Cmatch_plant_villageDlg::OnBnClickedButton1()
{
	// TODO: 在此添加控件通知处理程序代码
   
}
//开始扩充样本
void Cmatch_plant_villageDlg::OnBnClickedButton2()
{
	// TODO: 在此添加控件通知处理程序代码
}
