#include "userprofile.h"
#include "ui_userprofile.h"
#include <QFile>
#include <QTextStream>
#include <QDebug>
#include <QPalette>
#include <QPixmap>
#include "image.h"

userprofile::userprofile(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::userprofile)
{
    ui->setupUi(this);
    proc=new QProcess();
    showprocess=new QProcess();
    attri=new QProcess();

    connect(ui->next,SIGNAL(clicked()),this,SLOT(movenext()));
    connect(ui->back,SIGNAL(clicked()),this,SLOT(moveback()));
    connect(ui->generate,SIGNAL(clicked()),this,SLOT(generateuserprofile()));
    connect(proc,SIGNAL(finished(int)),this,SLOT(completed()));
    connect(showprocess,SIGNAL(finished(int)),this,SLOT(showcompleted()));
    connect(ui->show,SIGNAL(clicked()),this,SLOT(showclick()));
    connect(ui->zoom,SIGNAL(clicked()),this,SLOT(showimage()));
    connect(attri,SIGNAL(finished(int)),this,SLOT(attribshow()));
    connect(ui->img2zoom,SIGNAL(clicked()),this,SLOT(imgzoom()));
    connect(ui->attribute,SIGNAL(currentTextChanged(QString)),this,SLOT(attribchange()));


    //ui->next->setEnabled(false);

}

userprofile::~userprofile()
{
    delete ui;
}

void userprofile::movenext()
{
    emit moverecucedimension();
}

void userprofile::moveback()
{
    emit movebacktoupload();
}

void userprofile::generateuserprofile()
{

    QFile file("/home/rakesh/Qt/Reco/filename.txt");
    file.open(QIODevice::ReadOnly | QIODevice::Text);
    QTextStream in(&file);
    ui->scrollArea->setWidget(new QLabel ("running..."));
    QString item = in.readLine();



    QString param="python /home/rakesh/Qt/Reco/python/3_generateUP.py "+item;
    if(item.length()>0)
    {
qDebug()<<param;
    proc->start(param);}
    else{

    }

}

void userprofile::completed()
{
    qDebug()<<"end";
    ui->scrollArea->setWidget(new QLabel ("done. Files are created."));
    QFile file("/home/rakesh/Qt/Reco/python/movielens_1m_userlist.json");
    file.open(QIODevice::ReadOnly | QIODevice::Text);
    QTextStream in(&file);
    ui->userid->clear();
    while(!in.atEnd())   {
    QString item = in.readLine();
    ui->userid->addItem(item);
    qDebug()<<item;
    ui->next->setEnabled(true);
    }
}

void userprofile::showclick()
{
    QFile file1("/home/rakesh/Qt/Reco/filename.txt");
    file1.open(QIODevice::ReadOnly | QIODevice::Text);
    QTextStream in1(&file1);
    ui->scrollArea->setWidget(new QLabel ("running..."));
    QString item = in1.readLine();



    QString param="python /home/rakesh/Qt/Reco/python/3_show_attrib.py "+item+" "+ui->userid->currentText();
    if(item.length()>0)
    {
qDebug()<<param;
    showprocess->start(param);}
    else{

    }






}

void userprofile::showcompleted()
{
    qDebug()<<"end";
    //movielens_1m_userAttribImportance.png
    QFile file("/home/rakesh/Qt/Reco/python/db.txt");
            file.open(QIODevice::ReadOnly | QIODevice::Text);


            QTextStream in(&file);
            path= in.readLine();
            path=path+"/movielens_1m_userAttribImportance.png";
            qDebug()<<path;

            QPixmap pixmap(path);

            QSize size(ui->img1->width(),ui->img1->height());
            pixmap=pixmap.scaled(size);
            ui->img1->setPixmap(pixmap);


            qDebug()<<"attri closed";
    QFile file1("/home/rakesh/Qt/Reco/python/db.txt");
                file1.open(QIODevice::ReadOnly | QIODevice::Text);


                QTextStream in1(&file1);
                QString p= in1.readLine();
                p=p+"/movielens_1m_attributes.txt";
                QFile attribute(p);
                attribute.open(QIODevice::ReadOnly| QIODevice::Text);

                QTextStream reader(&attribute);
                ui->attribute->clear();
                while(!reader.atEnd()){
                    QString item=reader.readLine();
                    ui->attribute->addItem(item);
                }


}

void userprofile::showimage()
{
    QProcess *p=new QProcess();
    QString k=" shotwell "+path;
    p->start(k);
}

void userprofile::attribshow()
{
    qDebug()<<"attri closed";
    QFile file("/home/rakesh/Qt/Reco/python/db.txt");
                file.open(QIODevice::ReadOnly | QIODevice::Text);


                QTextStream in(&file);
                QString p= in.readLine();
                p=p+"/movielens_1m_userValueImportance.png";

                QPixmap pix(p);
                QSize size(ui->img2->width(),ui->img2->height());
                pix=pix.scaled(size);
                ui->img2->setPixmap(pix);
}

void userprofile::attribchange()
{

    QFile file1("/home/rakesh/Qt/Reco/filename.txt");
       file1.open(QIODevice::ReadOnly | QIODevice::Text);
       QTextStream in1(&file1);
       ui->scrollArea->setWidget(new QLabel ("running..."));
       QString item = in1.readLine();



       QString param="python /home/rakesh/Qt/Reco/python/3_show_value.py "+item+" "+ui->userid->currentText()+ " "+ui->attribute->currentText();
       if(item.length()>0)
       {
   qDebug()<<param;
       attri->start(param);}
       else{

       }



}

void userprofile::imgzoom()
{

        QFile file("/home/rakesh/Qt/Reco/python/db.txt");
                    file.open(QIODevice::ReadOnly | QIODevice::Text);


                    QTextStream in(&file);
                    QString p= in.readLine();
                    p=p+"/movielens_1m_userValueImportance.png";

                    QProcess *pro=new QProcess();
                    p="shotwell "+p;
                    pro->start(p);
}
