#include "upload.h"
#include "ui_upload.h"
#include <QFont>
#include <QFileDialog>
#include <QProcess>
#include <QDebug>
#include <QFile>
#include <QTextStream>
#include <QString>
#include <string>
upload::upload(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::upload)
{
    ui->setupUi(this);
    ui->scrollArea->setVisible(false);
    proc=new QProcess();
    item=QString();
    user= QString();
    connect(ui->itemupload,SIGNAL(clicked()),this,SLOT(itemupload()));


    connect(ui->next,SIGNAL(clicked()),this,SLOT(next()));
    connect(proc,SIGNAL(finished(int)),this,SLOT(completed()));


}

upload::~upload()
{
    qDebug()<<"deleted";
}

void upload::itemupload()
{
    QStringList fileNames = QFileDialog::getOpenFileNames(this, tr("Open File"),"/path/to/file/");
    if(fileNames.length()>0)
    {ui->itemedit->setText(fileNames[0]);
        item=fileNames[0];}
}

\

void upload::next()
{

    QString param="python /home/rakesh/Qt/Reco/python/2_verify_keyValueNode.py "+item;

    qDebug()<<item.lastIndexOf("/");

  qDebug()<<item.left(item.lastIndexOf("/"));

  QString filename=item.left(item.lastIndexOf("/"))+"/db.txt";
  QFile file(filename);
  file.open(QIODevice::WriteOnly | QIODevice::Text);
  QTextStream out(&file);
  out << item.left(item.lastIndexOf("/"));
  file.close();



     QFile file1("/home/rakesh/Qt/Reco/filename.txt");
    file1.open(QIODevice::WriteOnly | QIODevice::Text);
    QTextStream out1(&file1);
    out1 << item;
    file1.close();

    if(item.length()>0)
    {
    qDebug()<<param;
    proc->start(param);}
    else{
        QString l=QString("select a file");
        ui->scrollArea->setVisible(true);
        QLabel *label=new QLabel(l);
        ui->scrollArea->setWidget(label);
    }


}

void upload::completed()
{
    qDebug()<<"end";

    QFile file("/home/rakesh/Qt/Reco/python/movielens_1m_messages.log");
        file.open(QIODevice::ReadOnly | QIODevice::Text);


        QTextStream in(&file);
        QString line = in.readLine();
        QLabel *l=new QLabel(line);
        if(line.length()>0){
            ui->scrollArea->setVisible(true);
      ui->scrollArea->setWidget(l);}
        else{
            emit movenext();
        }


}
