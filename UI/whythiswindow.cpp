#include "whythiswindow.h"
#include "ui_whythiswindow.h"

whythiswindow::whythiswindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::whythiswindow)
{
    ui->setupUi(this);
    ml=new movielisty1();
    upl=new userproflisty2();
    dis=new displayy3();
    stackedwidget=new QStackedWidget();
    stackedwidget->addWidget(ml);
    stackedwidget->addWidget(upl);
    stackedwidget->addWidget(dis);
    stackedwidget->setCurrentIndex(0);

    connect(ml,SIGNAL(movenextwindow()),this,SLOT(movenext()));
    connect(upl,SIGNAL(movenext()),this,SLOT(movetwotothree()));

    this->setCentralWidget(stackedwidget);

}

whythiswindow::~whythiswindow()
{
    delete ui;
}

void whythiswindow::movenext()
{
    stackedwidget->setCurrentIndex(1);
}

void whythiswindow::movetwotothree()
{
    stackedwidget->setCurrentIndex(2);
}
