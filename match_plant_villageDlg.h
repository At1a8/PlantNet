
// match_plant_villageDlg.h : ͷ�ļ�
//

#pragma once
#include "cv.h"
#include "highgui.h"

// Cmatch_plant_villageDlg �Ի���
class Cmatch_plant_villageDlg : public CDialogEx
{
// ����
public:
	Cmatch_plant_villageDlg(CWnd* pParent = NULL);	// ��׼���캯��

// �Ի�������
	enum { IDD = IDD_MATCH_PLANT_VILLAGE_DIALOG };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV ֧��


// ʵ��
protected:
	HICON m_hIcon;

	// ���ɵ���Ϣӳ�亯��
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
