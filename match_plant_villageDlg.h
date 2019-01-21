
// match_plant_villageDlg.h : 头文件
//

#pragma once
#include "cv.h"
#include "highgui.h"

// Cmatch_plant_villageDlg 对话框
class Cmatch_plant_villageDlg : public CDialogEx
{
// 构造
public:
	Cmatch_plant_villageDlg(CWnd* pParent = NULL);	// 标准构造函数

// 对话框数据
	enum { IDD = IDD_MATCH_PLANT_VILLAGE_DIALOG };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV 支持


// 实现
protected:
	HICON m_hIcon;

	// 生成的消息映射函数
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	CString m_FilePath;
	afx_msg void OnBnClickedBtnSelectImagePath();
	afx_msg void OnBnClickedBtnCutImage();
	void imageProcess(CString imagePath);
	afx_msg void OnBnClickedButton1();
	afx_msg void OnBnClickedButton2();
};
