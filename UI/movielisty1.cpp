#include "movielisty1.h"
#include "ui_movielisty1.h"
#include <QFile>
#include <QTextStream>


movielisty1::movielisty1(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::movielisty1)
{
    ui->setupUi(this);
    QFile file("/home/rakesh/Qt/Reco/python/movielens_1m_uid_aplha");
                file.open(QIODevice::ReadOnly | QIODevice::Text);

                QString path;

                QTextStream in1(&file);
                path= in1.readLine();
                ui->Uidvalue->setText(path);


                QFile file1("/home/rakesh/Qt/Reco/python/movielens_1m_movieWatched.json");
                            file1.open(QIODevice::ReadOnly | QIODevice::Text);

                            QString path1;

                            QTextStream in(&file1);
                            path1= in.readLine();
                            ui->scrollArea->setWidget(new QLabel(path1));


                            QString path2;

                                path2="/home/rakesh/Qt/Reco/python/movielens_1m_Graph.png";



                                QPixmap p(path2);
                                QSize size(ui->img->width(),ui->img->height());
                                p=p.scaled(size);
                                ui->img->setPixmap(p);

                                connect(ui->Next,SIGNAL(clicked()),this,SLOT(movenext()));

}

movielisty1::~movielisty1()
{
    delete ui;
}

void movielisty1::movenext()
{emit movenextwindow();
}
