#include "reducedimension.h"
#include "ui_reducedimension.h"
#include <QFileDialog>
#include <QPalette>
#include <QDebug>
#include <QFile>

reduceDimension::reduceDimension(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::reduceDimension)
{
    ui->setupUi(this);
    proc=new QProcess();
    connect(ui->Reducedimension,SIGNAL(clicked()),this,SLOT(reducedimension()));
    connect(ui->back,SIGNAL(clicked()),this,SLOT(moveback()));
    connect(ui->next,SIGNAL(clicked()),this,SLOT(movenext()));
    connect(proc,SIGNAL(finished(int)),this,SLOT(reducedimover()));
    connect(ui->open,SIGNAL(clicked()),this,SLOT(open()));


}

reduceDimension::~reduceDimension()
{
    delete ui;
}

void reduceDimension::reducedimension()
{
    QFile file1("/home/rakesh/Qt/Reco/filename.txt");
        file1.open(QIODevice::ReadOnly | QIODevice::Text);
        QTextStream in1(&file1);

        QString item = in1.readLine();



        QString param="python /home/rakesh/Qt/Reco/python/4_reduceDimensions.py "+item;
        if(item.length()>0)
            {
        qDebug()<<param;
            proc->start(param);}
            else{

            }

          
}

void reduceDimension::moveback()
{
    qDebug()<<"came";
    emit movebacktouserprofile();
}

void reduceDimension::movenext()
{
    emit movetocomputesimilarity();
}

void reduceDimension::reducedimover()
{

QFile file("/home/rakesh/Qt/Reco/python/db.txt");
            file.open(QIODevice::ReadOnly | QIODevice::Text);


            QTextStream in(&file);
            path= in.readLine();
            path=path+"/movielens_1m_reducedDimension.png";
            qDebug()<<path;




 QPixmap pixmap1(path);



           QSize size(ui->image->width(), ui->image->height());
           //resize as per your requirement..
           pixmap1=(pixmap1.scaled(size));
           ui->image->setPixmap(pixmap1);
}

void reduceDimension::open()
{
    QFile file("/home/rakesh/Qt/Reco/python/db.txt");
                file.open(QIODevice::ReadOnly | QIODevice::Text);


                QTextStream in(&file);
                path= in.readLine();
                path=path+"/movielens_1m_reducedDimension.png";

                QProcess *p=new QProcess();
                path="shotwell "+path;
                p->start(path);

}

