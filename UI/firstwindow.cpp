#include "firstwindow.h"
#include "ui_firstwindow.h"
#include <QFont>

FirstWindow::FirstWindow(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::FirstWindow)
{
    ui->setupUi(this);

    up=new upload();

    QFont date=ui->Date->font();
    date.setPointSize(12);
    ui->Date->setFont(date);

    QFont algoname=ui->Algo->font();
    algoname.setPointSize(14);
    ui->Algo->setFont(algoname);

    QFont guide=ui->Guide->font();
    guide.setPointSize(12);
    ui->Guide->setFont(guide);

    QFont students=ui->students->font();
    students.setPointSize(12);
    ui->students->setFont(students);

    connect(ui->next,SIGNAL(clicked()),this,SLOT(next()));

}

FirstWindow::~FirstWindow()
{
    delete ui;
}

void FirstWindow::next()
{
    emit movenext();
}
